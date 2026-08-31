# -*- coding: utf-8 -*-
"""
coletor.py — Coletor da bacia do Alto Itajaí para GitHub Actions
Projeto: Previsão e Alerta de Cheia — CIDADE DE RIO DO SUL (SC)

Roda na nuvem do GitHub (PC desligado). Puxa as DUAS fontes públicas oficiais,
aplica a FUSÃO DE ESTAÇÕES por município (fusao_estacoes v0.3: média das réguas
pareadas, descarta sensor travado e 0,0 anômalo), roda o ESTIMADOR v0.9 em dois
modos (cj_v07 = OFICIAL/decide · cj_lat = SOMBRA com laterais) e decide se há
evento (para o workflow disparar o e-mail de alerta).

FONTES (públicas, sem login):
  1. ESTADO — monitoramento.defesacivil.sc.gov.br/graphql (client
     "secretaria-de-defesa-civil"): níveis + chuva de todas as estações.
  2. RIO DO SUL (Asthon) — public.asthon.com.br: barragens comporta a comporta.

Saídas (versionadas = histórico automático):
  dados/serie_bacia.csv   (append: 1 linha por ESTAÇÃO CRUA por coleta — auditoria)
  dados/niveis_bacia.csv  (append: 1 linha por COLETA, colunas = nível de cada
                           estação montante->jusante — p/ monitorar a onda)
  dados/barragens.csv     (append: barragens Sul/Oeste comporta a comporta)
  estado_atual.md         (situação + estimativa oficial e sombra, legível)
  evento.txt / assunto.txt (lidos pelo workflow p/ decidir/rotular o e-mail)

Só biblioteca padrão + estimador.py + fusao_estacoes.py (todos sem deps externas).
"""

import csv
import json
import os
import ssl
import statistics
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    import estimador
    import fusao_estacoes as fus
    TEM_MODELO = True
except Exception as _e:
    TEM_MODELO = False
    print(f"AVISO: estimador/fusao indisponível: {_e}", file=sys.stderr)

LOCAL = timezone(timedelta(hours=-3))
GQL = "https://monitoramento.defesacivil.sc.gov.br/graphql"
CLIENT = "secretaria-de-defesa-civil"
ASTHON = "https://public.asthon.com.br/public"
CITY = 4214805
UA = "Mozilla/5.0 (compatible; coletor-bacia-riodosul/2.0)"
DADOS = "dados"
LAG_MAX_MIN = 60   # R0: sensor com leitura mais velha que isso = TRAVADO (descartado)

# Estações a puxar (código DCSC 5 dígitos -> papel/nome), a partir do mapa
# canônico da fusão + as barragens. Se o módulo de fusão não carregar, cai
# num conjunto mínimo de exibição.
if TEM_MODELO:
    CODIGOS = sorted({c for _, cods in fus.MAPA_CJ.values() for c in cods}
                     | {"00038", "00040"})
else:
    CODIGOS = ["00013", "00039", "00041", "00033", "00025", "00035",
               "00010", "00016", "00038", "00040"]

# Ordem MONTANTE -> JUSANTE das estações COM régua de rio (só as já coletadas),
# usada no painel de níveis (dados/niveis_bacia.csv, formato largo). Ler a linha
# da esquerda p/ direita e, no tempo, de cima p/ baixo, mostra a onda "andando"
# pelo canal até a âncora (00013). Estações só-pluviômetro ficam de fora.
NIVEL_ORDEM = [
    # cabeceiras / montante
    ("00087", "Alfredo Wagner"),
    ("00125", "Rio do Campo"),
    ("00025", "Agrolandia"),
    # médio
    ("00067", "Aurora"),
    ("00065", "Salete"),
    ("00035", "Trombudo Central"),
    ("00086", "Atalanta"),
    # tronco médio / barragens
    ("00085", "Ituporanga H"),
    ("00039", "Ituporanga"),
    ("00038", "Barragem Sul"),
    ("00066", "Taio montante"),
    ("00171", "Taio H"),
    ("00041", "Taio"),
    ("00040", "Barragem Oeste"),
    # baixo / confluência
    ("00162", "Mirim Doce"),
    ("00022", "Rio do Oeste"),
    ("00179", "Rio do Oeste novo"),
    ("00033", "Pouso Redondo"),
    ("00031", "Laurentino"),
    ("00001", "Agronomica"),
    ("00146", "Petrolandia"),
    # âncora / tronco Rio do Sul
    ("00013", "Rio do Sul"),
]

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _post(url, payload, timeout=90):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
        headers={"content-type": "application/json", "user-agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url, timeout=90):
    req = urllib.request.Request(url, headers={"user-agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8"))


def _num(x, c=None):
    try:
        v = float(x)
        return round(v, c) if c is not None else v
    except (TypeError, ValueError):
        return None


def _dt_local_naive(ts_iso):
    """timestamp UTC do estado -> datetime NAIVE em horário local (-03)."""
    if not ts_iso:
        return None
    t = ts_iso.strip().replace(" ", "T").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(t).astimezone(LOCAL).replace(tzinfo=None)
    except ValueError:
        return None


_TAGS_Q = ('query Tags_data { tags_data(clients: ["%s"]) { qualle_meteorologia '
           '{ codigo name { general local } timestamp data { rio { rio_nivel '
           '{ value } rio_nivel_tendencia { value } } chuva { acumulado { '
           'h001 { value } h006 { value } h024 { value } h048 { value } '
           'h072 { value } } } } } } }') % CLIENT

_HIST_Q = ('query Historic($stationCode: String!, $startDate: String!, '
           '$endDate: String!, $interval: QueryInterval) { historic('
           'system: Qualle_Hidrometeorologia, client: "%s", '
           'stationCode: $stationCode, startDate: $startDate, '
           'endDate: $endDate, interval: $interval, opts: { ordenacao: ASC }) }') % CLIENT


def estado_bruto():
    """Retorna dict code5 -> {nome, ts(datetime naive local), nivel, tend, chNNh}."""
    d = _post(GQL, {"operationName": "Tags_data", "query": _TAGS_Q})
    est = (d.get("data") or {}).get("tags_data", {}).get("qualle_meteorologia", []) or []
    out = {}
    for e in est:
        if not e or not e.get("codigo"):
            continue
        code5 = e["codigo"].replace("DCSC-", "")
        rio = ((e.get("data") or {}).get("rio") or {})
        ac = (((e.get("data") or {}).get("chuva") or {}).get("acumulado") or {})
        def g(node, c=1):
            return _num((node or {}).get("value"), c) if node else None
        out[code5] = {
            "nome": (e.get("name") or {}).get("general") or "",
            "ts": _dt_local_naive(e.get("timestamp")),
            "nivel": g(rio.get("rio_nivel"), 2),
            "tend": g(rio.get("rio_nivel_tendencia"), 2),
            "ch1h": g(ac.get("h001")), "ch6h": g(ac.get("h006")),
            "ch24h": g(ac.get("h024")), "ch48h": g(ac.get("h048")),
            "ch72h": g(ac.get("h072")),
        }
    return out


def baseline_rds(horas=48):
    """Baseline pré-evento = MÍNIMO do nível de Rio do Sul nas últimas `horas`."""
    fim = datetime.now(timezone.utc)
    ini = fim - timedelta(hours=horas)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    d = _post(GQL, {"operationName": "Historic", "query": _HIST_Q,
                    "variables": {"stationCode": "DCSC-00013",
                                  "startDate": iso(ini), "endDate": iso(fim),
                                  "interval": "HOUR_1"}})
    itens = ((d.get("data") or {}).get("historic") or {}).get("items", []) or []
    niveis = [i.get("rio_nivel") for i in itens
              if isinstance(i.get("rio_nivel"), (int, float))]
    return round(min(niveis), 2) if niveis else None


def asthon_barragens():
    dados = _get(f"{ASTHON}/dams?city_id={CITY}")
    linhas = []
    for b in dados:
        ab, tot = b.get("comportas_abertas"), b.get("comportas_total")
        linhas.append({
            "barragem": b.get("name"),
            "medida_em": _dt_local_naive(b.get("measured_at")).strftime("%d/%m %H:%M")
                         if _dt_local_naive(b.get("measured_at")) else "",
            "percent_use": _num(b.get("percent_use"), 2),
            "vertido": b.get("vertido"),
            "comportas": f"{ab}A/{(tot or 0) - (ab or 0)}F",
            "montante_local_m": _num(b.get("nivel_m"), 2),
            "detalhe": ";".join(f"{c.get('nome')}:{'A' if c.get('aberta') else 'F'}"
                                for c in b.get("comportas", []) or []),
        })
    return linhas


def faixa_rds(n):
    if n is None:
        return "?"
    return ("EMERGÊNCIA" if n >= 6.5 else "ALERTA" if n >= 5.5
            else "ATENÇÃO" if n >= 4.5 else "Normal")


def _append(caminho, cabecalho, linhas):
    novo = not os.path.exists(caminho)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(cabecalho)
        w.writerows(linhas)


def _leituras(raw):
    """Constrói dict code5 -> fus.Leitura para o módulo de fusão."""
    out = {}
    for code5, s in raw.items():
        out[code5] = fus.Leitura(code5, s.get("ch48h"), s.get("nivel"), s.get("ts"))
    return out


def _stale(raw):
    """Lista de códigos com sensor TRAVADO (para avisar no md)."""
    ts = [s["ts"] for s in raw.values() if s.get("ts")]
    if not ts:
        return []
    ref = max(ts)
    fora = []
    for code5, s in raw.items():
        if code5 not in {c for _, cods in fus.MAPA_CJ.values() for c in cods}:
            continue
        if s.get("ts") is None or (ref - s["ts"]) > timedelta(minutes=LAG_MAX_MIN):
            fora.append(f"{code5} ({s.get('nome','?')})")
    return fora


# ---- FINO das barragens: derivação robusta do montante (peak-shaving) --------
GLITCH_M = 1.5            # salto de montante > isto num passo = degrau/glitch -> fora da taxa
DATUM_TOL_PP = 3.0       # tolerância da checagem de datum (curva V(h) x painel), pontos %
OCUP_TRAVA_CREDITO = 75.0  # salvaguarda JICA: >= isto, barragem não recebe crédito
JANELA_RETEN_H = getattr(estimador, "JANELA_PICO_H", 8.0) if TEM_MODELO else 8.0


def _barragens_hist(caminho):
    """Lê dados/barragens.csv -> {"Sul":[(dt,montante)], "Oeste":[...]} ordenado no tempo.
    Usa as colunas reais (coleta_local, barragem, montante_local_m)."""
    hist = {"Sul": [], "Oeste": []}
    if not os.path.exists(caminho):
        return hist
    try:
        with open(caminho, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                nb = row.get("barragem") or ""
                nome = "Sul" if "Sul" in nb else "Oeste" if "Oeste" in nb else None
                if not nome:
                    continue
                try:
                    dt = datetime.strptime(row["coleta_local"], "%Y-%m-%d %H:%M")
                    m = float(row["montante_local_m"])
                except (KeyError, ValueError, TypeError):
                    continue
                hist[nome].append((dt, m))
    except Exception:
        pass
    for k in hist:
        hist[k].sort(key=lambda x: x[0])
    return hist


def _derivar_montante(serie, horas=3.0):
    """Da série [(dt, montante)] devolve (fim, inicio, taxa_m_h, n) de forma ROBUSTA:
      - taxa = MEDIANA das variações sucessivas, ignorando degraus/glitches (|Δ|>GLITCH_M);
      - fim  = mediana das últimas 2-3 leituras (suaviza congelamento/spike);
      - inicio = fim − taxa × janela de retenção (8 h).
    Retorna None se houver < 3 leituras (cai no conservador)."""
    if not serie or len(serie) < 3:
        return None
    ult = serie[-1][0]
    janela = [(dt, m) for dt, m in serie if (ult - dt) <= timedelta(hours=horas)]
    if len(janela) < 3:
        janela = serie[-3:]
    if len(janela) < 3:
        return None
    fim = statistics.median([m for _, m in janela[-3:]])
    taxas = []
    for (t0, m0), (t1, m1) in zip(janela, janela[1:]):
        dt_h = (t1 - t0).total_seconds() / 3600.0
        if dt_h <= 0:
            continue
        dh = m1 - m0
        if abs(dh) > GLITCH_M:      # degrau (congelou e pulou) -> não conta na taxa
            continue
        taxas.append(dh / dt_h)
    taxa = statistics.median(taxas) if taxas else 0.0
    inicio = fim - taxa * JANELA_RETEN_H
    return fim, inicio, taxa, len(janela)


def _montar_barragens(dams, hist_bar):
    """Constrói (conserv_bars, fino_bars, cred) — cada barragem em 2 versões:
    CONSERVADOR (montante 0,0 -> retenção 0) e FINO (montante ini/fim derivados,
    com as salvaguardas dos passos 3-4). `cred` traz o detalhe por barragem."""
    conserv_bars, fino_bars, cred = [], [], []
    for d in dams:
        nb = d.get("barragem") or ""
        nome = "Sul" if "Sul" in nb else "Oeste" if "Oeste" in nb else None
        if not nome:
            continue
        pct = d.get("percent_use")
        vert = d.get("vertido") or 0
        ext = float(vert) if isinstance(vert, (int, float)) and vert > 0 else 0.0
        conserv_bars.append(estimador.BarragemV5(nome, 0.0, 0.0,
                            ocupacao_pct=pct, extravasor_m=ext))

        info = {"nome": nome, "occ_pct": pct, "credito_ok": False, "motivo": "",
                "montante_fim": None, "montante_ini": None, "taxa": None,
                "occ_curva": None, "vol_hm3": 0.0, "q_m3s": 0.0}
        der = _derivar_montante(hist_bar.get(nome, []))
        verting = (ext > 0) or (isinstance(pct, (int, float)) and pct >= 100)
        if der is None:
            info["motivo"] = "histórico de montante insuficiente (<3 leituras) — conservador"
        else:
            fim, ini, taxa, n = der
            info.update(montante_fim=round(fim, 2), montante_ini=round(ini, 2),
                        taxa=round(taxa, 3))
            occ_curva = estimador.ocupacao_de_montante(nome, fim)
            info["occ_curva"] = round(occ_curva, 1)
            datum_ok = (pct is not None) and abs(occ_curva - pct) <= DATUM_TOL_PP
            # ordem das salvaguardas (passos 3-4 + vertimento)
            if verting:
                info["motivo"] = "vertendo/extravasor ativo — água-acima transita, sem crédito"
            elif isinstance(pct, (int, float)) and pct >= OCUP_TRAVA_CREDITO:
                info["motivo"] = (f"ocupação {pct}% ≥ {OCUP_TRAVA_CREDITO:.0f}% "
                                  "(salvaguarda JICA) — sem crédito")
            elif taxa <= 0:
                info["motivo"] = "não está enchendo (taxa ≤ 0) — sem crédito"
            elif not datum_ok:
                info["motivo"] = (f"datum montante suspeito (curva {occ_curva:.1f}% vs "
                                  f"painel {pct}% > {DATUM_TOL_PP:.0f}pp) — usando conservador")
            else:
                info["credito_ok"] = True

        if info["credito_ok"]:
            b = estimador.BarragemV5(nome, info["montante_ini"], info["montante_fim"],
                                     ocupacao_pct=pct, extravasor_m=ext)
            info["vol_hm3"] = round(b.volume_retido_hm3, 2)
            info["q_m3s"] = round(b.q_retencao_m3s, 0)
        else:
            # sem crédito: montante_fim == inicio -> retenção 0, mas preserva ocupacao_pct
            mf = info["montante_fim"] if info["montante_fim"] is not None else 0.0
            b = estimador.BarragemV5(nome, mf, mf, ocupacao_pct=pct, extravasor_m=ext)
        fino_bars.append(b)
        cred.append(info)
    return conserv_bars, fino_bars, cred


def _resumo_est(e):
    return {"pico": round(e.pico_central, 1),
            "banda": (round(e.banda[0], 1), round(e.banda[1], 1)),
            "faixa": e.faixa, "cj": round(e.cj_efetiva_mm, 0),
            "nota_bar": e.nota_barragens, "ant": e.antecedencia_h}


def estimar(raw, dams):
    """Roda o estimador v0.9 em CONSERVADOR (guarda) e FINO (crédito de retenção
    real das barragens, derivado do montante de dados/barragens.csv). Retorna dict."""
    if not TEM_MODELO:
        return None
    try:
        base = baseline_rds()
        if base is None:
            base = raw.get("00013", {}).get("nivel")
        if base is None:
            return None
        leit = _leituras(raw)
        chuvas_v07, chuvas_lat = fus.dicts_para_estimador(leit)
        duplo = fus.cj_duplo(leit)

        hist_bar = _barragens_hist(os.path.join(DADOS, "barragens.csv"))
        conserv_bars, fino_bars, cred = _montar_barragens(dams, hist_bar)
        # fallback global de SEGURANÇA: qualquer barragem sem crédito (ou nenhuma barragem)
        fallback_global = (not cred) or any(not c["credito_ok"] for c in cred)

        # usar_ancoras=False: DRIVERS (v0.9) já inclui âncoras + laterais.
        of_c = estimador.estimar_pico_v5(base, chuvas_v07, conserv_bars, usar_ancoras=False)
        of_f = estimador.estimar_pico_v5(base, chuvas_v07, fino_bars, usar_ancoras=False)
        sh = estimador.estimar_pico_v5(base, chuvas_lat, fino_bars, usar_ancoras=False)

        # Classe que dispara o alerta: FINO, exceto se houver fallback -> CONSERVADOR
        # (nunca rebaixar um alerta silenciosamente enquanto a retenção não é comprovada).
        classe_alerta = of_c.faixa if fallback_global else of_f.faixa

        return {
            "baseline": base,
            "conserv": _resumo_est(of_c),
            "fino": _resumo_est(of_f),
            "sombra": {"pico": round(sh.pico_central, 1), "cj": round(sh.cj_efetiva_mm, 0)},
            "duplo": duplo,
            "chuvas_v07": chuvas_v07,
            "cred": cred,
            "fallback_global": fallback_global,
            "classe_alerta": classe_alerta,
        }
    except Exception as e:
        print(f"AVISO estimador: {e}", file=sys.stderr)
        return None


def main():
    os.makedirs(DADOS, exist_ok=True)
    agora = datetime.now(LOCAL)
    ts = agora.strftime("%Y-%m-%d %H:%M")

    erros = []
    try:
        raw = estado_bruto()
    except Exception as e:
        raw = {}; erros.append(f"estado(Qualle): {e}")
    try:
        dams = asthon_barragens()
    except Exception as e:
        dams = []; erros.append(f"barragens(Asthon): {e}")

    # --- série CRUA por estação (auditoria; granularidade preservada) ---
    linhas = []
    for code5 in CODIGOS:
        s = raw.get(code5, {})
        linhas.append([ts, "DCSC-" + code5, s.get("nome", ""),
                       s["ts"].strftime("%Y-%m-%d %H:%M") if s.get("ts") else "",
                       s.get("nivel"), s.get("tend"), s.get("ch1h"),
                       s.get("ch24h"), s.get("ch48h"), s.get("ch72h")])
    _append(os.path.join(DADOS, "serie_bacia.csv"),
            ["coleta_local", "codigo", "nome", "leitura", "nivel_m", "tendencia",
             "chuva_1h", "chuva_24h", "chuva_48h", "chuva_72h"], linhas)

    # --- painel de NÍVEIS (formato largo: 1 linha por coleta, colunas
    # montante->jusante) — para monitorar a onda subindo/descendo o canal ---
    cab_niv = ["coleta_local"] + [f"{c} {rot}" for c, rot in NIVEL_ORDEM]
    linha_niv = [ts] + [
        (raw.get(c, {}).get("nivel") if raw.get(c, {}).get("nivel") is not None
         else "") for c, _ in NIVEL_ORDEM
    ]
    _append(os.path.join(DADOS, "niveis_bacia.csv"), cab_niv, [linha_niv])

    if dams:
        _append(os.path.join(DADOS, "barragens.csv"),
                ["coleta_local", "barragem", "medida_em", "percent_use", "vertido",
                 "comportas", "montante_local_m", "detalhe"],
                [[ts, d["barragem"], d["medida_em"], d["percent_use"], d["vertido"],
                  d["comportas"], d["montante_local_m"], d["detalhe"]] for d in dams])

    # --- estado + gatilho de evento ---
    rds = raw.get("00013", {})
    niv = rds.get("nivel")
    faixa = faixa_rds(niv)
    subindo = (rds.get("tend") or 0) > 0
    # chuva 24h máx entre os municípios-driver (dado cru, p/ responsividade)
    driver_codes = []
    if TEM_MODELO:
        for muni, (papel, cods) in fus.MAPA_CJ.items():
            if papel in ("ancora", "driver"):
                driver_codes += cods
    ch24max = max([raw.get(c, {}).get("ch24h") or 0 for c in driver_codes] or [0])
    vertendo = any((x.get("percent_use") or 0) >= 100 or x.get("vertido") for x in dams)

    est = estimar(raw, dams)
    stale = _stale(raw) if (TEM_MODELO and raw) else []

    # Classe que dispara o alerta = FINO (retenção real), ou CONSERVADOR se houver
    # fallback de barragem. O gatilho de evento nunca é REBAIXADO pelo fino: mantém
    # os gatilhos atuais (nível/chuva) e SOMA a classe prevista.
    classe_alerta = est["classe_alerta"] if est else faixa
    evento = (faixa in ("ATENÇÃO", "ALERTA", "EMERGÊNCIA")
              or (subindo and ch24max >= 30) or ch24max >= 50
              or classe_alerta in ("ATENÇÃO", "ALERTA", "EMERGÊNCIA"))

    # --- estado_atual.md ---
    md = [f"# Cheia — Rio do Sul (SC) — {ts} (local −03)", ""]
    md.append(f"**Rio do Sul (00013):** {niv} m — **{faixa}** · "
              f"tendência {'subindo' if subindo else 'estável/caindo'}")
    md.append(f"**Chuva 24h máx (drivers):** {round(ch24max,1)} mm")
    md.append(f"**EVENTO ATIVO:** {'🔴 SIM' if evento else '🟢 não'}")
    if evento and est:
        fn = est["fino"]; cs = est["conserv"]; s = est["sombra"]; dpl = est["duplo"]
        flo, fhi = fn["banda"]; clo, chi = cs["banda"]
        usa_cons = est["fallback_global"]
        md.append("")
        md.append(f"**Pico estimado (FINO — c/ retenção real das barragens):** "
                  f"~{fn['pico']} m (banda {flo}–{fhi} m) → **{fn['faixa']}**")
        md.append(f"**Guarda (CONSERVADOR — sem crédito de retenção):** "
                  f"~{cs['pico']} m (banda {clo}–{chi} m) → **{cs['faixa']}**")
        md.append(f"**Classe que dispara o alerta/e-mail: {est['classe_alerta']}** — "
                  + ("usando o CONSERVADOR (há fallback de barragem; o fino não "
                     "rebaixa alerta enquanto a retenção não é comprovada)."
                     if usa_cons else
                     "usando o FINO (retenção comprovada nas barragens)."))
        md.append(f"- baseline (mín 48h): {est['baseline']} m · "
                  f"chuva-jusante efetiva: {fn['cj']:.0f} mm · "
                  f"antecedência ~{fn['ant'][0]}–{fn['ant'][1]} h")
        md.append(f"- sombra (cj_lat, c/ laterais): ~{s['pico']} m "
                  f"(cj {s['cj']:.0f} mm · Δcj_lat−cj_v07 = "
                  f"{dpl.get('delta')} mm, n_laterais={dpl.get('n_lat_validas')})")
        md += ["", "### Crédito de retenção por barragem (peak-shaving)", "",
               "| Barragem | Ocupação | Montante ini→fim (m) | Taxa (m/h) | "
               "Retido (hm³) | Corte (m³/s) | Crédito |",
               "|---|---|---|---|---|---|---|"]
        for cc in est["cred"]:
            mont = (f"{cc['montante_ini']}→{cc['montante_fim']}"
                    if cc.get("montante_fim") is not None else "—")
            occ = f"{cc['occ_pct']}%" + (f" (curva {cc['occ_curva']}%)"
                                         if cc.get("occ_curva") is not None else "")
            if cc["credito_ok"]:
                credito = "✅ aplicado"
            else:
                credito = f"⚠ 0 — {cc['motivo']}"
            md.append(f"| {cc['nome']} | {occ} | {mont} | {cc.get('taxa')} | "
                      f"{cc['vol_hm3']} | {cc['q_m3s']} | {credito} |")
        md.append(f"- termo de barragem (fino): {fn['nota_bar']}")
    if est and est.get("chuvas_v07"):
        cv = est["chuvas_v07"]
        drv = {k: v for k, v in cv.items() if k in getattr(estimador, "DRIVERS", [])}
        aci = {k: v for k, v in cv.items() if k in getattr(estimador, "ACIMA", [])}
        md += ["", "## Chuva-jusante fundida (48h) — entra no cj oficial",
               "", "| Município | Chuva 48h (mm) |", "|---|---|"]
        for muni, v in sorted(drv.items(), key=lambda kv: -kv[1]):
            md.append(f"| {muni} | {v:.1f} |")
        if aci:
            md += ["", "_Chuva-acima (contexto de barragem, fora do cj):_ "
                   + ", ".join(f"{k} {v:.1f}" for k, v in sorted(aci.items(), key=lambda kv: -kv[1]))]
    if dams:
        md += ["", "## Barragens (Asthon)", "",
               "| Barragem | % uso | Comportas | Vertido | Montante |", "|---|---|---|---|---|"]
        for d in dams:
            md.append(f"| {d['barragem']} | {d['percent_use']} | {d['comportas']} "
                      f"| {d['vertido']} | {d['montante_local_m']} m |")
    avisos = list(erros)
    if stale:
        avisos.append("Sensores TRAVADOS (descartados na fusão): " + ", ".join(stale))
    if avisos:
        md += ["", "## ⚠ Avisos desta coleta", ""] + [f"- {a}" for a in avisos]
    with open("estado_atual.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    with open("evento.txt", "w", encoding="utf-8") as f:
        f.write("SIM" if evento else "NAO")

    pico_fino = est["fino"]["pico"] if est else None
    assunto = (f"[CHEIA {classe_alerta}] Rio do Sul {niv} m"
               + (f" · pico~{pico_fino} m" if evento and pico_fino is not None else "")) if evento \
              else f"[ok] Rio do Sul normal — {niv} m"
    with open("assunto.txt", "w", encoding="utf-8") as f:
        f.write(assunto)

    print(f"EVENTO={'SIM' if evento else 'NAO'} | Rio do Sul {niv} m [{faixa}] "
          f"| chuva24h máx {round(ch24max,1)} mm"
          + (f" | FINO ~{pico_fino} m / guarda ~{est['conserv']['pico']} m "
             f"[alerta {classe_alerta}]" if est else ""))
    if avisos:
        print("AVISOS:", "; ".join(avisos), file=sys.stderr)

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"evento={'SIM' if evento else 'NAO'}\n")
            f.write(f"assunto={assunto}\n")

    if not raw and not dams:
        print("FALHA: nenhuma fonte respondeu.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
