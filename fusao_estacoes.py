"""
fusao_estacoes_v0_3.py
----------------------
v0.3 (calibracao prospectiva): cj_duplo() e dicts_para_estimador() — cada
evento novo registra o PAR (cj_v07 sem laterais, cj_lat com laterais);
o estimador roda nas duas versoes (v07 DECIDE; lat = modo SOMBRA) ate a
base pareada permitir recalibracao pre-registrada.
----------------------
v0.2 (opcao 2): incluir_laterais=True por DEFAULT — laterais entram na media
cj operacional, casando com estimador v0.9 (DRIVERS+4).
----------------------
Fusão de estações por município para montar o dicionário de chuva que o
estimador_pico consome (chaves = nomes de município das listas ANCORAS/
DRIVERS/ACIMA).

Regras travadas em 28/08/2026 (fonte: decisões Jonevaldo desta sessão):

R0  Descarte por sensor TRAVADO: estação cuja "Última Atualização" está
    defasada mais que `lag_max_min` em relação à leitura mais recente da
    rede é ignorada (chuva E nível). É o caso 00022 hoje (27/08 08:57).

R1  Taió separa os lados da barragem: a âncora cj usa só o par JUSANTE
    (00041 + 00171). 00066 (entrada = montante) NÃO entra no cj; vai para
    chuva-acima Oeste como linha própria (chave "Taio_montante"),
    separada de Rio do Campo.

R2  Descarte de 0,00 SÓ na chuva e SÓ quando anômalo: numa cidade com duas
    leituras, descarta a que ler 0,0 enquanto a irmã tiver volume
    >= `limiar_signif` mm. Se as duas lerem 0,0 (dia seco), mantém as duas
    (cj = 0,0 é válido). NÍVEL de rio nunca entra nesse descarte.

Fusão = MÉDIA das leituras sobreviventes do município.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# MAPA CANÔNICO município -> (papel_cj, [códigos a mediar])
# papel_cj: "ancora" | "driver" | "acima"
# Só entram no cj de pico as chaves ancora/driver. "acima" é contexto.
# ----------------------------------------------------------------------
MAPA_CJ: dict[str, tuple[str, list[str]]] = {
    # jusante — entram no cj
    "Rio do Sul":        ("ancora", ["00013"]),
    "Ituporanga":        ("ancora", ["00085", "00039"]),
    "Taio":              ("ancora", ["00041", "00171"]),   # só jusante
    "Aurora":            ("driver", ["00067", "00008"]),
    "Salete":            ("driver", ["00065"]),
    "Rio do Oeste":      ("driver", ["00022", "00179"]),
    "Laurentino":        ("driver", ["00031"]),
    "Pouso Redondo":     ("driver", ["00033"]),
    "Agrolandia":        ("driver", ["00025"]),
    "Trombudo Central":  ("driver", ["00035", "00014"]),
    "Agronomica":        ("driver", ["00001"]),
    # laterais não controladas, jusante — chuva-jusante física, singletons.
    # NÃO entram na média DRIVERS calibrada por default (ver montar_cj):
    # entram só se incluir_laterais=True (dispara recalibração/LOO).
    "Petrolandia":       ("lateral", ["00146"]),   # Perimbó, abaixo da Sul
    "Atalanta":          ("lateral", ["00086"]),   # abaixo de 00085; checar vitalidade
    "Mirim Doce":        ("lateral", ["00162"]),   # foz <50 m abaixo de 00041
    "Braco do Trombudo": ("lateral", ["00129"]),   # eixo Trombudo, 100% não controlado
    # montante — chuva-acima, fora do cj de pico
    "Alfredo Wagner":    ("acima",  ["00016", "00087"]),
    "Rio do Campo":      ("acima",  ["00010", "00125"]),
    "Taio_montante":     ("acima",  ["00066"]),            # anotado à parte
}


@dataclass
class Leitura:
    codigo: str
    chuva_mm: float | None      # None = célula "-" (sem dado)
    rio_m: float | None
    atualizado: datetime


def _frescor_rede(leituras: dict[str, Leitura]) -> datetime:
    ts = [l.atualizado for l in leituras.values() if l.atualizado is not None]
    return max(ts) if ts else datetime.min


def _travada(l: Leitura, ref: datetime, lag_max_min: int) -> bool:
    if l.atualizado is None:
        return True
    return (ref - l.atualizado) > timedelta(minutes=lag_max_min)


def fundir_chuva(municipio: str,
                 leituras: dict[str, Leitura],
                 ref_frescor: datetime,
                 lag_max_min: int = 60,
                 limiar_signif: float = 5.0) -> tuple[float | None, list[str]]:
    """Retorna (chuva_fundida_mm, log). None se nenhuma estação sobreviver."""
    papel, codigos = MAPA_CJ[municipio]
    log: list[str] = []
    vivos: list[tuple[str, float]] = []

    for c in codigos:
        l = leituras.get(c)
        if l is None or l.chuva_mm is None:
            log.append(f"{c}: sem dado -> fora")
            continue
        if _travada(l, ref_frescor, lag_max_min):
            log.append(f"{c}: TRAVADA ({l.atualizado:%d/%m %H:%M}) -> fora")
            continue
        vivos.append((c, l.chuva_mm))

    if not vivos:
        return None, log

    # R2: descarte de 0,0 anômalo (só se algum vivo tem volume significativo)
    if len(vivos) > 1 and any(v >= limiar_signif for _, v in vivos):
        filtrados = [(c, v) for c, v in vivos if v > 0.0]
        for c, v in vivos:
            if v == 0.0:
                log.append(f"{c}: 0,0 anômalo (irmã >= {limiar_signif}) -> fora")
        vivos = filtrados if filtrados else vivos

    valor = sum(v for _, v in vivos) / len(vivos)
    usados = "+".join(c for c, _ in vivos)
    log.append(f"chuva fundida = média({usados}) = {valor:.1f} mm")
    return valor, log


def fundir_nivel(municipio: str,
                 leituras: dict[str, Leitura],
                 ref_frescor: datetime,
                 lag_max_min: int = 60) -> tuple[float | None, list[str]]:
    """Nível: só descarta TRAVADA. Nunca aplica R2 (0,0 anômalo)."""
    _, codigos = MAPA_CJ[municipio]
    log: list[str] = []
    vivos: list[tuple[str, float]] = []
    for c in codigos:
        l = leituras.get(c)
        if l is None or l.rio_m is None:
            continue
        if _travada(l, ref_frescor, lag_max_min):
            log.append(f"{c}: TRAVADA -> fora (nível)")
            continue
        vivos.append((c, l.rio_m))
    if not vivos:
        return None, log
    valor = sum(v for _, v in vivos) / len(vivos)
    log.append(f"nível fundido = média({'+'.join(c for c,_ in vivos)}) = {valor:.2f} m")
    return valor, log


def montar_cj(leituras: dict[str, Leitura],
              incluir_laterais: bool = True, **kw) -> dict[str, float]:
    """Monta o dict {municipio: chuva_mm} para o estimador.

    Default v0.2: ancora+driver+LATERAL (opcao 2 executada; estimador v0.9).
    incluir_laterais=True adiciona Petrolândia/Atalanta/Mirim Doce/Braço do
    Trombudo — muda a média DRIVERS e EXIGE recalibração/LOO antes de confiar
    na sensibilidade. 'acima' nunca entra."""
    papeis = {"ancora", "driver"} | ({"lateral"} if incluir_laterais else set())
    ref = _frescor_rede(leituras)
    out: dict[str, float] = {}
    for muni, (papel, _) in MAPA_CJ.items():
        if papel not in papeis:
            continue
        val, _ = fundir_chuva(muni, leituras, ref, **kw)
        if val is not None:
            out[muni] = val
    return out


def laterais_avulsas(leituras: dict[str, Leitura], **kw) -> dict[str, float]:
    """Canal paralelo: chuva fundida das laterais, para exibir/observar sem
    contaminar a média calibrada. Use enquanto a recalibração não fecha."""
    ref = _frescor_rede(leituras)
    out: dict[str, float] = {}
    for muni, (papel, _) in MAPA_CJ.items():
        if papel != "lateral":
            continue
        val, _ = fundir_chuva(muni, leituras, ref, **kw)
        if val is not None:
            out[muni] = val
    return out


# ----------------------------------------------------------------------
# v0.3 — CALIBRACAO PROSPECTIVA (dupla escrituracao por evento)
# ----------------------------------------------------------------------
def montar_acima(leituras: dict[str, Leitura], **kw) -> dict[str, float]:
    """Dict {municipio: chuva_mm} das chaves de chuva-ACIMA (contexto de
    barragem; inclui Taio_montante). Junta-se aos dicts do cj p/ o estimador."""
    ref = _frescor_rede(leituras)
    out: dict[str, float] = {}
    for muni, (papel, _) in MAPA_CJ.items():
        if papel != "acima":
            continue
        val, _ = fundir_chuva(muni, leituras, ref, **kw)
        if val is not None:
            out[muni] = val
    return out


def cj_duplo(leituras: dict[str, Leitura], **kw) -> dict:
    """PAR de cj do protocolo prospectivo (Instrucoes v24):
      cj_v07 — media flat do conjunto ancora+driver ANTIGO (continuidade com
               a curva calibrada 0,48; e o numero que DECIDE na operacao);
      cj_lat — media com as LATERAIS dentro (novo conjunto; modo SOMBRA);
      delta  — cj_lat − cj_v07 (a grandeza que a base pareada acumula).
    A ficha de cada evento novo registra AMBOS + laterais individuais."""
    d07 = montar_cj(leituras, incluir_laterais=False, **kw)
    dlat = montar_cj(leituras, incluir_laterais=True, **kw)
    cj07 = round(sum(d07.values()) / len(d07), 1) if d07 else None
    cjlat = round(sum(dlat.values()) / len(dlat), 1) if dlat else None
    return {
        "cj_v07": cj07, "cj_lat": cjlat,
        "delta": round(cjlat - cj07, 2) if None not in (cj07, cjlat) else None,
        "n_v07": len(d07), "n_lat_total": len(dlat),
        "n_lat_validas": len(dlat) - len(d07),
        "laterais": laterais_avulsas(leituras, **kw),
    }


def dicts_para_estimador(leituras: dict[str, Leitura], **kw
                         ) -> tuple[dict, dict]:
    """(chuvas_v07, chuvas_lat) prontos p/ estimar_pico_v5, JA com as chaves
    de chuva-acima. Protocolo: rodar o estimador DUAS vezes —
      chuvas_v07 -> previsao OFICIAL (curva calibrada; decide);
      chuvas_lat -> previsao SOMBRA (erro logado a parte p/ a base pareada)."""
    acima = montar_acima(leituras, **kw)
    chuvas_v07 = montar_cj(leituras, incluir_laterais=False, **kw) | acima
    chuvas_lat = montar_cj(leituras, incluir_laterais=True, **kw) | acima
    return chuvas_v07, chuvas_lat
