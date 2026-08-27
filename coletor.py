# -*- coding: utf-8 -*-
"""
coletor.py — Coletor da bacia do Alto Itajaí (Rio do Sul) para GitHub Actions
Projeto: Previsão e Alerta de Cheia / 100 Frescura

Roda na nuvem do GitHub (PC desligado) a cada 30 min. Puxa as DUAS fontes
públicas oficiais, acumula a série em dados/ e decide se há evento (para o
workflow disparar o e-mail de alerta).

FONTES (ambas públicas, sem login):
  1. ESTADO — monitoramento.defesacivil.sc.gov.br/graphql (plataforma "Qualle")
     client="secretaria-de-defesa-civil". Níveis + chuva de TODAS as estações
     da bacia (inclui Ituporanga 00039 e Taió 00041, que a Asthon não tem).
  2. RIO DO SUL (Asthon) — public.asthon.com.br/public (REST) — barragens
     comporta a comporta (% ocupação, comportas A/F, montante).

Saídas (versionadas no repositório = histórico automático dos eventos):
  dados/serie_bacia.csv    (append: 1 linha por estação por coleta)
  dados/barragens.csv      (append: 1 linha por barragem por coleta)
  estado_atual.md          (sobrescrito: situação atual legível no GitHub)
  evento.txt               ("SIM"/"NAO" — lido pelo workflow p/ decidir e-mail)

Só biblioteca padrão (urllib). Sem 'pip install'.
"""

import csv
import json
import os
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

LOCAL = timezone(timedelta(hours=-3))
GQL = "https://monitoramento.defesacivil.sc.gov.br/graphql"
CLIENT = "secretaria-de-defesa-civil"
ASTHON = "https://public.asthon.com.br/public"
CITY = 4214805
UA = "Mozilla/5.0 (compatible; coletor-bacia-100frescura/1.0)"

DADOS = "dados"

# Estações da bacia que alimentam o modelo (código DCSC do site estadual)
ALVO = {
    "DCSC-00013": "Rio do Sul (âncora)",
    "DCSC-00039": "Ituporanga cidade",
    "DCSC-00041": "Taió cidade",
    "DCSC-00001": "Agronômica",
    "DCSC-00022": "Rio do Oeste",
    "DCSC-00025": "Agrolândia",
    "DCSC-00031": "Laurentino",
    "DCSC-00033": "Pouso Redondo",
    "DCSC-00014": "Trombudo Central 1",
    "DCSC-00035": "Trombudo Central 2",
    "DCSC-00010": "Rio do Campo",
    "DCSC-00016": "Alfredo Wagner",
    "DCSC-00024": "Vidal Ramos",
    "DCSC-00008": "Aurora",
    "DCSC-00038": "Barragem Sul (montante)",
    "DCSC-00040": "Barragem Oeste (montante)",
}
# drivers de chuva a jusante das barragens (para o gatilho de evento)
DRIVERS = ["DCSC-00013", "DCSC-00039", "DCSC-00041", "DCSC-00033",
           "DCSC-00025", "DCSC-00010", "DCSC-00016"]

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


def _ts_local(ts_iso):
    if not ts_iso:
        return ""
    t = ts_iso.strip().replace(" ", "T").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(t).astimezone(LOCAL).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return ts_iso


_TAGS_Q = ('query Tags_data { tags_data(clients: ["%s"]) { qualle_meteorologia '
           '{ codigo name { general local } timestamp data { rio { rio_nivel '
           '{ value } rio_nivel_tendencia { value } } chuva { acumulado { '
           'h001 { value } h006 { value } h024 { value } h048 { value } '
           'h072 { value } } } } } } }') % CLIENT


def estado_snapshot():
    d = _post(GQL, {"operationName": "Tags_data", "query": _TAGS_Q})
    est = (d.get("data") or {}).get("tags_data", {}).get("qualle_meteorologia", []) or []
    out = {}
    for e in est:
        if not e or not e.get("codigo"):
            continue
        rio = ((e.get("data") or {}).get("rio") or {})
        ac = (((e.get("data") or {}).get("chuva") or {}).get("acumulado") or {})
        def g(node, c=1):
            return _num((node or {}).get("value"), c) if node else None
        out[e["codigo"]] = {
            "nome": (e.get("name") or {}).get("general") or "",
            "ts": _ts_local(e.get("timestamp")),
            "nivel": g(rio.get("rio_nivel"), 2),
            "tend": g(rio.get("rio_nivel_tendencia"), 2),
            "ch1h": g(ac.get("h001")), "ch6h": g(ac.get("h006")),
            "ch24h": g(ac.get("h024")), "ch48h": g(ac.get("h048")),
            "ch72h": g(ac.get("h072")),
        }
    return out


def asthon_barragens():
    dados = _get(f"{ASTHON}/dams?city_id={CITY}")
    linhas = []
    for b in dados:
        ab, tot = b.get("comportas_abertas"), b.get("comportas_total")
        linhas.append({
            "barragem": b.get("name"),
            "medida_em": _ts_local(b.get("measured_at")),
            "percent_use": _num(b.get("percent_use"), 2),
            "vertido": b.get("vertido"),
            "comportas": f"{ab}A/{(tot or 0) - (ab or 0)}F",
            "montante_local_m": _num(b.get("nivel_m"), 2),
            "detalhe": ";".join(f"{c.get('nome')}:{'A' if c.get('aberta') else 'F'}"
                                for c in b.get("comportas", []) or []),
        })
    return linhas


def _append(caminho, cabecalho, linhas):
    novo = not os.path.exists(caminho)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(cabecalho)
        w.writerows(linhas)


def faixa_rds(n):
    if n is None:
        return "?"
    return ("EMERGÊNCIA" if n >= 6.5 else "ALERTA" if n >= 5.5
            else "ATENÇÃO" if n >= 4.5 else "Normal")


def main():
    os.makedirs(DADOS, exist_ok=True)
    agora = datetime.now(LOCAL)
    ts = agora.strftime("%Y-%m-%d %H:%M")

    erros = []
    try:
        snap = estado_snapshot()
    except Exception as e:
        snap = {}; erros.append(f"estado(Qualle): {e}")
    try:
        dams = asthon_barragens()
    except Exception as e:
        dams = []; erros.append(f"barragens(Asthon): {e}")

    # append série das estações-alvo
    linhas = []
    for code, papel in ALVO.items():
        s = snap.get(code, {})
        linhas.append([ts, code, papel, s.get("ts", ""), s.get("nivel"),
                       s.get("tend"), s.get("ch1h"), s.get("ch6h"),
                       s.get("ch24h"), s.get("ch48h"), s.get("ch72h")])
    _append(os.path.join(DADOS, "serie_bacia.csv"),
            ["coleta_local", "codigo", "papel", "leitura", "nivel_m", "tendencia",
             "chuva_1h", "chuva_6h", "chuva_24h", "chuva_48h", "chuva_72h"], linhas)

    if dams:
        _append(os.path.join(DADOS, "barragens.csv"),
                ["coleta_local", "barragem", "medida_em", "percent_use", "vertido",
                 "comportas", "montante_local_m", "detalhe"],
                [[ts, d["barragem"], d["medida_em"], d["percent_use"], d["vertido"],
                  d["comportas"], d["montante_local_m"], d["detalhe"]] for d in dams])

    # avaliação de evento
    rds = snap.get("DCSC-00013", {})
    niv = rds.get("nivel")
    faixa = faixa_rds(niv)
    ch24max = max([snap.get(c, {}).get("ch24h") or 0 for c in DRIVERS] or [0])
    subindo = (rds.get("tend") or 0) > 0
    vertendo = any((x.get("percent_use") or 0) >= 100 or x.get("vertido") for x in dams)
    evento = (faixa in ("ATENÇÃO", "ALERTA", "EMERGÊNCIA")
              or (subindo and ch24max >= 30) or ch24max >= 50)
    cjv = [snap.get(c, {}).get("ch48h") or 0 for c in ["DCSC-00013", "DCSC-00039", "DCSC-00041"]]
    cj = sum(cjv) / len(cjv) if cjv else 0
    pico = round(2.29 + 0.59 * niv + 0.032 * cj + (1.0 if vertendo else 0.0), 1) if niv is not None else None

    # estado_atual.md
    md = [f"# Estado da bacia — {ts} (local −03)", ""]
    md.append(f"**Rio do Sul:** {niv} m — **{faixa}** · "
              f"tendência {'subindo' if subindo else 'estável/caindo'}")
    md.append(f"**Chuva 24h máx (drivers):** {round(ch24max,1)} mm")
    md.append(f"**EVENTO ATIVO:** {'🔴 SIM' if evento else '🟢 não'}")
    if evento and pico is not None:
        md.append(f"**Pico estimado (heurística):** ~{pico} m "
                  f"(nível inicial {niv} + chuva média 48h {round(cj,1)} mm"
                  f"{' + vertimento' if vertendo else ''})")
    md += ["", "## Estações", "", "| Código | Estação | Nível (m) | Chuva 24h |",
           "|---|---|---|---|"]
    for code, papel in ALVO.items():
        s = snap.get(code, {})
        md.append(f"| {code} | {papel} | {s.get('nivel') if s.get('nivel') is not None else '—'} "
                  f"| {s.get('ch24h') if s.get('ch24h') is not None else '—'} |")
    if dams:
        md += ["", "## Barragens (Asthon)", "",
               "| Barragem | % uso | Comportas | Vertido | Montante |", "|---|---|---|---|---|"]
        for d in dams:
            md.append(f"| {d['barragem']} | {d['percent_use']} | {d['comportas']} "
                      f"| {d['vertido']} | {d['montante_local_m']} m |")
    if erros:
        md += ["", "## ⚠ Avisos desta coleta", ""] + [f"- {e}" for e in erros]
    with open("estado_atual.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    with open("evento.txt", "w", encoding="utf-8") as f:
        f.write("SIM" if evento else "NAO")

    # resumo p/ o assunto do e-mail e o log do Actions
    assunto = (f"[CHEIA {faixa}] Rio do Sul {niv} m"
               + (f" · pico~{pico} m" if evento and pico is not None else "")) if evento \
              else f"[ok] bacia normal — Rio do Sul {niv} m"
    with open("assunto.txt", "w", encoding="utf-8") as f:
        f.write(assunto)

    print(f"EVENTO={'SIM' if evento else 'NAO'} | Rio do Sul {niv} m [{faixa}] "
          f"| chuva24h máx {round(ch24max,1)} mm"
          + (f" | pico~{pico} m" if evento and pico is not None else ""))
    if erros:
        print("AVISOS:", "; ".join(erros), file=sys.stderr)

    # expõe saídas para o workflow (GITHUB_OUTPUT)
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"evento={'SIM' if evento else 'NAO'}\n")
            f.write(f"assunto={assunto}\n")

    # se ambas as fontes falharem, sai com erro (job vermelho = você percebe)
    if not snap and not dams:
        print("FALHA: nenhuma fonte respondeu.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
