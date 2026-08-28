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
  dados/barragens.csv     (append: barragens Sul/Oeste comporta a comporta)
  estado_atual.md         (situação + estimativa oficial e sombra, legível)
  evento.txt / assunto.txt (lidos pelo workflow p/ decidir/rotular o e-mail)

Só biblioteca padrão + estimador.py + fusao_estacoes.py (todos sem deps externas).
"""

import csv
import json
import os
import ssl
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

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE


def _post(url, payload, timeout=45):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data,
        headers={"content-type": "application/json", "user-agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
        return json.loads(r.read().decode("utf-8"))


def _get(url, timeout=45):
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


def estimar(raw, dams):
    """Roda o estimador v0.9 nos dois modos. Retorna dict ou None."""
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
        bars = []
        for d in dams:
            nb = d.get("barragem") or ""
            nome = "Sul" if "Sul" in nb else "Oeste" if "Oeste" in nb else None
            if not nome:
                continue
            vert = d.get("vertido") or 0
            ext = float(vert) if isinstance(vert, (int, float)) and vert > 0 else 0.0
            bars.append(estimador.BarragemV5(nome, 0.0, 0.0,
                        ocupacao_pct=d.get("percent_use"), extravasor_m=ext))
        # usar_ancoras=False: a lista DRIVERS (v0.9) já inclui âncoras + laterais,
        # então chuvas_v07 -> cj oficial (sem laterais) e chuvas_lat -> cj sombra.
        of = estimador.estimar_pico_v5(base, chuvas_v07, bars, usar_ancoras=False)
        sh = estimador.estimar_pico_v5(base, chuvas_lat, bars, usar_ancoras=False)
        return {
            "baseline": base,
            "oficial": {"pico": round(of.pico_central, 1),
                        "banda": (round(of.banda[0], 1), round(of.banda[1], 1)),
                        "faixa": of.faixa, "cj": round(of.cj_efetiva_mm, 0),
                        "nota_bar": of.nota_barragens, "ant": of.antecedencia_h},
            "sombra": {"pico": round(sh.pico_central, 1),
                       "cj": round(sh.cj_efetiva_mm, 0)},
            "duplo": duplo,
            "chuvas_v07": chuvas_v07,
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
    evento = (faixa in ("ATENÇÃO", "ALERTA", "EMERGÊNCIA")
              or (subindo and ch24max >= 30) or ch24max >= 50)

    est = estimar(raw, dams)
    stale = _stale(raw) if (TEM_MODELO and raw) else []

    # --- estado_atual.md ---
    md = [f"# Cheia — Rio do Sul (SC) — {ts} (local −03)", ""]
    md.append(f"**Rio do Sul (00013):** {niv} m — **{faixa}** · "
              f"tendência {'subindo' if subindo else 'estável/caindo'}")
    md.append(f"**Chuva 24h máx (drivers):** {round(ch24max,1)} mm")
    md.append(f"**EVENTO ATIVO:** {'🔴 SIM' if evento else '🟢 não'}")
    if evento and est:
        o = est["oficial"]; s = est["sombra"]; dpl = est["duplo"]
        lo, hi = o["banda"]
        md.append("")
        md.append(f"**Pico estimado (OFICIAL, v0.9 cj_v07):** ~{o['pico']} m "
                  f"(banda {lo}–{hi} m) → **{o['faixa']}**")
        md.append(f"- baseline (mín 48h): {est['baseline']} m · "
                  f"chuva-jusante efetiva: {o['cj']:.0f} mm · "
                  f"antecedência ~{o['ant'][0]}–{o['ant'][1]} h")
        md.append(f"- **sombra (cj_lat, c/ laterais):** ~{s['pico']} m "
                  f"(cj {s['cj']:.0f} mm · Δcj_lat−cj_v07 = "
                  f"{dpl.get('delta')} mm, n_laterais={dpl.get('n_lat_validas')})")
        md.append(f"- barragens: {o['nota_bar']}")
        md.append("- *barragens em modo conservador (sem crédito de peak-shaving "
                  "volumétrico; para o número fino, rodar o estimador à mão).*")
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

    pico_of = est["oficial"]["pico"] if est else None
    assunto = (f"[CHEIA {faixa}] Rio do Sul {niv} m"
               + (f" · pico~{pico_of} m" if evento and pico_of is not None else "")) if evento \
              else f"[ok] Rio do Sul normal — {niv} m"
    with open("assunto.txt", "w", encoding="utf-8") as f:
        f.write(assunto)

    print(f"EVENTO={'SIM' if evento else 'NAO'} | Rio do Sul {niv} m [{faixa}] "
          f"| chuva24h máx {round(ch24max,1)} mm"
          + (f" | pico oficial ~{pico_of} m (sombra ~{est['sombra']['pico']} m)"
             if est else ""))
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
