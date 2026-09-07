# -*- coding: utf-8 -*-
"""
coletor.py — Coletor da bacia do Alto Itajaí para GitHub Actions
Projeto: Previsão e Alerta de Cheia — CIDADE DE RIO DO SUL (SC)

Roda na nuvem do GitHub (PC desligado). Puxa as DUAS fontes públicas oficiais,
aplica a FUSÃO DE ESTAÇÕES por município (fusao_estacoes v0.3: média das réguas
pareadas, descarta sensor travado e 0,0 anômalo), roda o ESTIMADOR v1.0
(estimador.py) com as grandezas DO ATO — baseline no VALE detectado na régua,
chuva-jusante somada hora a hora DESDE O VALE (não o rolante 48 h), volume retido
nas barragens desde o vale e fração de comportas abertas — em dois modos
(cj_v07 = OFICIAL/decide · cj_lat = SOMBRA com laterais), guarda a previsão do
v0.9 antigo para comparação e decide se há evento (e-mail de alerta).

MODO CRISTA (nowcast na fase final): quando a chuva-driver encerrou E as réguas-
líder (Pouso Redondo/Trombudo/Agrolândia) já cristaram E o rio ainda sobe mas
DESACELERA, o número principal passa a ser a PROJEÇÃO DA TRAJETÓRIA
(projetar_crista_pos_chuva, validado −0,03/+0,02 nos ev.15/16) e o v1.0 vira TETO.
Doutrina Instruções v27 §E / v28 D-CRISTA: perto da crista o modelo "chuva entra,
pico sai" perde para a trajetória observada. A classe do alerta segue a projeção,
nunca abaixo da faixa atual do rio.

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
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

try:
    import estimador                 # v1.0 (estimador_pico_v1_0.py) — OFICIAL
    import fusao_estacoes as fus
    TEM_MODELO = True
except Exception as _e:
    TEM_MODELO = False
    print(f"AVISO: estimador/fusao indisponível: {_e}", file=sys.stderr)
try:
    import estimador_v09             # modelo antigo (v0.9) — só comparação no md
except Exception:
    estimador_v09 = None

LOCAL = timezone(timedelta(hours=-3))
GQL = "https://monitoramento.defesacivil.sc.gov.br/graphql"
CLIENT = "secretaria-de-defesa-civil"
ASTHON = "https://public.asthon.com.br/public"
CITY = 4214805
UA = "Mozilla/5.0 (compatible; coletor-bacia-riodosul/2.0)"
DADOS = "dados"
LAG_MAX_MIN = 60   # R0: sensor com leitura mais velha que isso = TRAVADO (descartado)

# ---- REFERÊNCIA DE NÍVEL DE RIO DO SUL --------------------------------------
# Toda a calibração do projeto (limiares 4,5/5,5/6,5, baseline, estimador) é
# referenciada à régua da DEFESA CIVIL DE RIO DO SUL (Ponte Dom Tito Buss), que
# hoje vive na Asthon e lê ~0,24 m ABAIXO da SDC-00013. A SDC vinha inflando o
# nível. Rollback trivial: troque para "SDC" e volta o comportamento antigo.
REFERENCIA_NIVEL = "DC_RS"   # "DC_RS" (Asthon Ponte Dom Tito) | "SDC" (DCSC-00013)
DOMTITO_UUID = "f6360951-219f-4859-935f-b2e2d13962f1"   # DC-RS Ponte Dom Tito Buss
KANITZ_UUID = "30475400-b7ba-4551-9646-19df0c3bfa38"    # Ponte Ricardo Kanitz (checagem)
OFFSET_SEMENTE = -0.24       # dc_rs − sdc medido (DC-RS mais baixa); só semente do fallback
OFFSET_JANELA_H = 48         # janela p/ a mediana do offset de fallback

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


def asthon_estacoes_live():
    """dict uuid -> {'level': m, 'em': 'dd/mm HH:MM', 'em_dt': datetime} (Asthon live)."""
    out = {}
    try:
        for e in _get(f"{ASTHON}/stations/live?city_id={CITY}"):
            uid = e.get("station_id")
            if not uid:
                continue
            em = _dt_local_naive(e.get("last_reading_at"))
            out[uid] = {"level": _num(e.get("level_m"), 2),
                        "em": em.strftime("%d/%m %H:%M") if em else "", "em_dt": em}
    except Exception as ex:
        print(f"AVISO asthon live: {ex}", file=sys.stderr)
    return out


def asthon_nivel_hist(uuid, horas=48):
    """[(dt_local_naive, level)] das últimas `horas` de uma estação Asthon (ordenado)."""
    fim = datetime.now(timezone.utc)
    ini = fim - timedelta(hours=horas)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    qs = urllib.parse.urlencode({"station_id": uuid, "start": iso(ini),
                                 "end": iso(fim), "fields": "level"})
    out = []
    try:
        d = _get(f"{ASTHON}/station-history?{qs}")
        for p in d.get("level") or []:
            dt = _dt_local_naive(p.get("timestamp"))
            v = p.get("value")
            if dt is not None and isinstance(v, (int, float)):
                out.append((dt, float(v)))
    except Exception as ex:
        print(f"AVISO asthon hist {uuid[:8]}: {ex}", file=sys.stderr)
    out.sort(key=lambda x: x[0])
    return out


def _ultima_linha(caminho):
    """Última linha (dict) de um CSV com cabeçalho; None se vazio/ausente."""
    if not os.path.exists(caminho):
        return None
    try:
        with open(caminho, encoding="utf-8") as f:
            linhas = list(csv.DictReader(f))
        return linhas[-1] if linhas else None
    except Exception:
        return None


def offset_fallback(caminho, horas=OFFSET_JANELA_H):
    """Mediana do offset_medido_m das últimas `horas` de nivel_rds.csv; senão semente."""
    if not os.path.exists(caminho):
        return OFFSET_SEMENTE
    corte = datetime.now(LOCAL).replace(tzinfo=None) - timedelta(hours=horas)
    vals = []
    try:
        with open(caminho, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    dt = datetime.strptime(row["coleta_local"], "%Y-%m-%d %H:%M")
                    off = float(row["offset_medido_m"])
                except (KeyError, ValueError, TypeError):
                    continue
                if dt >= corte:
                    vals.append(off)
    except Exception:
        pass
    return round(statistics.median(vals), 3) if vals else OFFSET_SEMENTE


def resolver_referencia(sdc_niv, sdc_tend, base_sdc, dom_live, dom_hist, off_fb):
    """Decide nível/baseline/tendência de referência conforme REFERENCIA_NIVEL, com
    fallback DC-RS -> SDC+offset. Retorna dict (nivel, baseline, subindo, fonte, obs,
    dc_rs, sdc, offset_medido). NUNCA fica sem nível se a SDC existir."""
    dc_rs = dom_live
    offset_medido = (round(dc_rs - sdc_niv, 3)
                     if (dc_rs is not None and sdc_niv is not None) else None)
    base_dc = round(min(v for _, v in dom_hist), 2) if dom_hist else None
    # tendência DC-RS pela inclinação da última ~1h do histórico Asthon
    subindo_dc = None
    if len(dom_hist) >= 2:
        ult_dt, ult_v = dom_hist[-1]
        ref_pt = next(((dt, v) for dt, v in reversed(dom_hist)
                       if (ult_dt - dt) >= timedelta(minutes=45)), dom_hist[0])
        subindo_dc = (ult_v - ref_pt[1]) > 0.0

    if REFERENCIA_NIVEL == "SDC":
        return {"nivel": sdc_niv, "baseline": base_sdc, "subindo": (sdc_tend or 0) > 0,
                "fonte": "SDC-00013", "obs": "", "dc_rs": dc_rs, "sdc": sdc_niv,
                "offset_medido": offset_medido}

    if dc_rs is not None:   # DC-RS disponível
        base = base_dc if base_dc is not None else (
            round(base_sdc + off_fb, 2) if base_sdc is not None else None)
        obs = "" if base_dc is not None else f"baseline via SDC+offset ({off_fb})"
        subindo = subindo_dc if subindo_dc is not None else (sdc_tend or 0) > 0
        return {"nivel": dc_rs, "baseline": base, "subindo": subindo,
                "fonte": "DC-RS (Asthon Ponte Dom Tito)", "obs": obs,
                "dc_rs": dc_rs, "sdc": sdc_niv, "offset_medido": offset_medido}

    # DC-RS indisponível -> SDC + offset (sinalizado)
    niv = round(sdc_niv + off_fb, 2) if sdc_niv is not None else None
    base = round(base_sdc + off_fb, 2) if base_sdc is not None else None
    return {"nivel": niv, "baseline": base, "subindo": (sdc_tend or 0) > 0,
            "fonte": f"SDC+offset (DC-RS indisponível, off={off_fb})",
            "obs": "DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset",
            "dc_rs": None, "sdc": sdc_niv, "offset_medido": None}


def faixa_rds(n):
    if n is None:
        return "?"
    return ("EMERGÊNCIA" if n >= 6.5 else "ALERTA" if n >= 5.5
            else "ATENÇÃO" if n >= 4.5 else "Normal")


import unicodedata as _ud
_ORD_FAIXA = {"NORMAL": 0, "ATENCAO": 1, "ALERTA": 2, "EMERGENCIA": 3, "": 0}

def _rank_faixa(f):
    """Severidade da faixa (0 Normal .. 3 Emergência), robusta a caixa/acento/'?'."""
    k = "".join(c for c in _ud.normalize("NFD", (f or "").upper()) if c.isalpha())
    return _ORD_FAIXA.get(k, 0)

def _mais_severa(a, b):
    return a if _rank_faixa(a) >= _rank_faixa(b) else b

def _e_alerta(f):
    return _rank_faixa(f) >= 1


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


# ---- ESTIMADOR v1.0: janela do ATO (vale -> agora) --------------------------
# O v1.0 (estimador.py) é alimentado com grandezas DO ATO, não com acumulados
# rolantes: cj = soma horária desde o VALE; ΔV = volume retido nas barragens
# desde o vale (pelas % da Asthon); fração de comportas abertas desde o vale.
VALE_SOBE_MIN = 0.25      # m — subida que separa um ato do anterior (detecção do vale)
VALE_MAX_H = 96           # h — quanto olhar para trás ao procurar o vale
COBERTURA_MIN = 0.7       # fração das horas do ato com snapshot p/ usar a soma horária
VOL_TOTAL = {"Sul": 104.03, "Oeste": 99.96}   # hm³ (painel, ev.14)

# ---- MODO CRISTA (nowcast na fase final; doutrina v27 §E: perto da crista o número
# vem da TRAJETÓRIA observada, o v1.0 vira teto) ----------------------------------
CRISTA_CHUVA_MAX = 2.0    # mm/h — chuva-driver acima disso = ainda chovendo (não ativa)
CRISTA_JANELA_H = 2.0     # h — janela p/ medir a taxa de subida atual e a anterior
CRISTA_TAXA_MIN = 0.02    # m/h — subida abaixo disso = crista essencialmente atingida
CRISTA_SALTO_MAX = 0.5    # m — degrau horário maior que isso = spike/manobra -> não ativa
CRISTA_LIDERES = {"00033": "Pouso Redondo", "00035": "Trombudo Central", "00025": "Agrolandia"}


def _mediana3(hist):
    """Filtro de mediana (janela 3) na série [(dt, v)] — tira spikes de sensor."""
    if len(hist) < 3:
        return list(hist)
    out = [hist[0]]
    for i in range(1, len(hist) - 1):
        out.append((hist[i][0], statistics.median([hist[i-1][1], hist[i][1], hist[i+1][1]])))
    out.append(hist[-1])
    return out


def detectar_vale(hist, sobe_min=VALE_SOBE_MIN, max_h=VALE_MAX_H):
    """VALE do ato atual (baseline do estimador = disciplina de baseline do projeto):
    andando para trás a partir de agora, o vale é o mínimo encontrado ANTES de o rio
    voltar a ficar mais de `sobe_min` acima dele (= recessão do ato anterior).
    Num 2º/3º ato devolve o trough (convenção J2); numa subida única, o baseline
    pré-evento. hist = [(dt_local_naive, nivel)] ordenado. Retorna (dt, nivel) ou None."""
    h = _mediana3([(dt, v) for dt, v in hist if v is not None])
    if not h:
        return None
    cur_dt, cur = h[-1]
    vale_dt, vale = cur_dt, cur
    for dt, v in reversed(h):
        if (cur_dt - dt) > timedelta(hours=max_h):
            break
        if v <= vale:
            vale, vale_dt = v, dt
        elif v > vale + sobe_min and (vale_dt - dt) >= timedelta(hours=2):
            break
    return vale_dt, round(vale, 2)


def historico_sdc(horas=VALE_MAX_H):
    """[(dt_local_naive, nivel)] do DCSC-00013 (Historic HOUR_1) nas últimas `horas`."""
    fim = datetime.now(timezone.utc)
    ini = fim - timedelta(hours=horas)
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    d = _post(GQL, {"operationName": "Historic", "query": _HIST_Q,
                    "variables": {"stationCode": "DCSC-00013",
                                  "startDate": iso(ini), "endDate": iso(fim),
                                  "interval": "HOUR_1"}})
    itens = ((d.get("data") or {}).get("historic") or {}).get("items", []) or []
    out = []
    for i in itens:
        v = i.get("rio_nivel")
        t = i.get("timestamp") or i.get("data") or i.get("date")
        if not isinstance(v, (int, float)):
            continue
        dt = None
        if isinstance(t, str):
            try:   # o Historic devolve horário LOCAL (Instruções: "ts local")
                dt = datetime.fromisoformat(t.replace("Z", "").replace(" ", "T")[:19])
            except ValueError:
                dt = _dt_local_naive(t)
        if dt is not None:
            out.append((dt, float(v)))
    out.sort(key=lambda x: x[0])
    return out


def _ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def chuva_ato_estacoes(caminho, t_vale, agora):
    """Soma HORÁRIA da chuva de cada estação desde o vale, a partir do histórico do
    próprio coletor (dados/serie_bacia.csv, coluna chuva_1h = acumulado da última
    hora na leitura da estação). Um snapshot por hora de leitura (o mais recente
    dentro da hora) evita sobreposição entre coletas de 30 min.
    Retorna (dict code5 -> mm, cobertura 0..1, n_horas)."""
    horas = max(1.0, (agora - t_vale).total_seconds() / 3600.0)
    por_est = {}
    for row in _ler_csv(caminho):
        try:
            code5 = (row.get("codigo") or "").replace("DCSC-", "")
            leit = datetime.strptime(row["leitura"], "%Y-%m-%d %H:%M")
            ch = float(row["chuva_1h"])
        except (KeyError, ValueError, TypeError):
            continue
        if leit <= t_vale or leit > agora + timedelta(minutes=30):
            continue
        balde = leit.replace(minute=0, second=0, microsecond=0)
        d = por_est.setdefault(code5, {})
        if balde not in d or leit > d[balde][0]:
            d[balde] = (leit, ch)
    soma = {c: round(sum(v for _, v in d.values()), 1) for c, d in por_est.items()}
    n_h = max((len(d) for d in por_est.values()), default=0)
    cobertura = min(1.0, n_h / horas)
    return soma, cobertura, n_h


def _acumulado_rolante(s, horas):
    """Fallback: acumulado do painel cuja janela cobre as horas desde o vale."""
    for h, k in ((6, "ch6h"), (24, "ch24h"), (48, "ch48h"), (72, "ch72h")):
        if horas <= h:
            return s.get(k), k
    return s.get("ch72h"), "ch72h"


def _leituras_ato(raw, t_vale, agora):
    """dict code5 -> fus.Leitura com a CHUVA DO ATO (soma horária desde o vale;
    fallback = acumulado rolante do painel com a janela mais próxima). Retorna
    (leituras, metodo, cobertura)."""
    horas = max(1.0, (agora - t_vale).total_seconds() / 3600.0)
    soma, cob, n_h = chuva_ato_estacoes(os.path.join(DADOS, "serie_bacia.csv"), t_vale, agora)
    usar_soma = cob >= COBERTURA_MIN and n_h >= 2
    out = {}
    janela = None
    for code5, s in raw.items():
        if usar_soma and code5 in soma:
            ch = soma[code5]
        else:
            ch, janela = _acumulado_rolante(s, horas)
        out[code5] = fus.Leitura(code5, ch, s.get("nivel"), s.get("ts"))
    metodo = (f"soma horária desde o vale ({n_h} h, cobertura {cob:.0%})" if usar_soma
              else f"acumulado rolante {janela or '?'} do painel (histórico do ato insuficiente: "
                   f"{n_h} h, cobertura {cob:.0%})")
    return out, metodo, cob


def _comportas(txt):
    """'3A/2F' -> (abertas, total)"""
    try:
        a, f = txt.upper().replace(" ", "").split("/")
        a, f = int(a.rstrip("A")), int(f.rstrip("F"))
        return a, a + f
    except Exception:
        return None, None


def barragens_ato(caminho, dams, t_vale, agora):
    """Estado das barragens NO ATO, por dados/barragens.csv + leitura atual (Asthon):
    % no vale, % agora, ΔV retido (hm³), fração média de comportas ABERTAS desde o
    vale, vertendo. Retorna lista de dicts (Sul, Oeste)."""
    hist = {"Sul": [], "Oeste": []}
    for row in _ler_csv(caminho):
        nb = row.get("barragem") or ""
        nome = "Sul" if "Sul" in nb else "Oeste" if "Oeste" in nb else None
        if not nome:
            continue
        try:
            dt = datetime.strptime(row["coleta_local"], "%Y-%m-%d %H:%M")
        except (KeyError, ValueError, TypeError):
            continue
        pct = _num(row.get("percent_use"))
        ab, tot = _comportas(row.get("comportas") or "")
        hist[nome].append((dt, pct, ab, tot))
    for k in hist:
        hist[k].sort(key=lambda x: x[0])

    out = []
    for d in dams:
        nb = d.get("barragem") or ""
        nome = "Sul" if "Sul" in nb else "Oeste" if "Oeste" in nb else None
        if not nome:
            continue
        pct_agora = d.get("percent_use")
        vert = d.get("vertido") or 0
        vertendo = (isinstance(vert, (int, float)) and vert > 0) or \
                   (isinstance(pct_agora, (int, float)) and pct_agora >= 100)
        h = hist[nome]
        obs = ""
        antes = [x for x in h if x[0] <= t_vale and x[1] is not None]
        if antes:
            pct_vale = antes[-1][1]
        elif h and h[0][1] is not None:
            pct_vale = h[0][1]
            obs = f"histórico começa depois do vale ({h[0][0]:%d/%m %H:%M}) — ΔV pode estar subestimado"
        else:
            pct_vale = pct_agora
            obs = "sem histórico de barragem — ΔV = 0"
        dv = 0.0
        if isinstance(pct_agora, (int, float)) and isinstance(pct_vale, (int, float)):
            dv = max(0.0, (pct_agora - pct_vale) / 100.0 * VOL_TOTAL[nome])
        # fração aberta ponderada no tempo desde o vale (função-degrau) + estado atual
        pontos = [(dt, ab / tot) for dt, _, ab, tot in h if dt >= t_vale and ab is not None and tot]
        ab_now, tot_now = _comportas(d.get("comportas") or "")
        if ab_now is not None and tot_now:
            pontos.append((agora, ab_now / tot_now))
        if pontos:
            prev = [(dt, ab / tot) for dt, _, ab, tot in h if dt < t_vale and ab is not None and tot]
            f0 = prev[-1][1] if prev else pontos[0][1]
            seq = [(t_vale, f0)] + pontos
            acc = tot_h = 0.0
            for (t0, f), (t1, _) in zip(seq, seq[1:]):
                dh = max(0.0, (t1 - t0).total_seconds() / 3600.0)
                acc += f * dh; tot_h += dh
            fracao = round(acc / tot_h, 2) if tot_h > 0 else pontos[-1][1]
        else:
            fracao = None
        out.append({"nome": nome, "pct_vale": pct_vale, "pct_agora": pct_agora, "dv_hm3": round(dv, 1),
                    "fracao_aberta": fracao, "vertendo": vertendo, "comportas": d.get("comportas"),
                    "montante": d.get("montante_local_m"), "obs": obs})
    return out


def _resumo_v1(e):
    return {"pico": round(e.pico_central, 1),
            "banda": (round(e.banda[0], 1), round(e.banda[1], 1)),
            "faixa": e.faixa, "cj_ef": round(e.cj_efetiva_mm, 0),
            "termos": e.termos, "classe_banda": e.classe_banda}


def _serie_estacao(caminho, code5, horas, agora, col="nivel_m", tcol="coleta_local"):
    """[(dt, valor)] de uma estação em dados/serie_bacia.csv nas últimas `horas`."""
    out = []
    for row in _ler_csv(caminho):
        if (row.get("codigo") or "").replace("DCSC-", "") != code5:
            continue
        try:
            dt = datetime.strptime(row[tcol], "%Y-%m-%d %H:%M")
            v = float(row[col])
        except (KeyError, ValueError, TypeError):
            continue
        if timedelta(0) <= (agora - dt) <= timedelta(hours=horas):
            out.append((dt, v))
    out.sort(key=lambda x: x[0])
    return out


def _taxa(hist, t0, t1):
    """Taxa média (m/h) entre os pontos da série [(dt,v)] mais próximos de t0 e t1."""
    if len(hist) < 2:
        return None
    near = lambda t: min(hist, key=lambda pt: abs((pt[0] - t).total_seconds()))
    (ta, va), (tb, vb) = near(t0), near(t1)
    dh = (tb - ta).total_seconds() / 3600.0
    return (vb - va) / dh if abs(dh) >= 0.5 else None


def _lider_cristou(caminho, code5, agora, horas=3.0):
    """True/False se a régua-líder já virou (nível caindo no período); None sem dado."""
    h = _mediana3(_serie_estacao(caminho, code5, horas + 1, agora, col="nivel_m", tcol="coleta_local"))
    if len(h) < 3:
        return None
    return (h[-1][1] - h[0][1]) < -0.02


def _chuva_driver_recente(caminho, agora, horas=2.0):
    """Máx de chuva_1h entre as estações-driver nas últimas `horas` (mm/h); None sem dado."""
    if not TEM_MODELO:
        return None
    driver5 = {c for muni, (papel, cods) in fus.MAPA_CJ.items()
               if papel in ("ancora", "driver") for c in cods}
    mx, achou = 0.0, False
    for row in _ler_csv(caminho):
        code5 = (row.get("codigo") or "").replace("DCSC-", "")
        if code5 not in driver5:
            continue
        try:
            dt = datetime.strptime(row["leitura"], "%Y-%m-%d %H:%M")
            ch = float(row["chuva_1h"])
        except (KeyError, ValueError, TypeError):
            continue
        if timedelta(0) <= (agora - dt) <= timedelta(hours=horas):
            mx = max(mx, ch); achou = True
    return mx if achou else None


def modo_crista(ref_hist, caminho, niv, agora, teto_v1_0=None):
    """Nowcast da crista na fase final do evento. Ativa quando, ao mesmo tempo:
      (a) o rio ainda sobe mas DESACELERA (2ª diferença negativa), ou já virou;
      (b) a chuva-driver ENCERROU (máx chuva_1h ≤ CRISTA_CHUVA_MAX nas últimas 2 h);
      (c) as réguas-líder (Pouso Redondo/Trombudo/Agrolândia) já CRISTARAM.
    Doutrina (Instruções v27 §E / v28 D-CRISTA): perto da crista o número vem da
    TRAJETÓRIA (projetar_crista_pos_chuva, validado −0,03/+0,02 nos ev.15/16); o
    estimador v1.0 vira TETO. Retorna dict ou None (condições não satisfeitas)."""
    if not TEM_MODELO or niv is None or not ref_hist or len(ref_hist) < 4:
        return None
    h = _mediana3([(dt, v) for dt, v in ref_hist if v is not None])
    if len(h) < 4:
        return None
    t = h[-1][0]
    if abs(h[-1][1] - h[-2][1]) > CRISTA_SALTO_MAX:      # degrau/manobra/spike -> aguarda
        return None
    taxa = _taxa(h, t - timedelta(hours=CRISTA_JANELA_H), t)
    taxa_prev = _taxa(h, t - timedelta(hours=2 * CRISTA_JANELA_H), t - timedelta(hours=CRISTA_JANELA_H))
    if taxa is None or taxa_prev is None:
        return None
    subindo = taxa > CRISTA_TAXA_MIN
    desacelera = taxa < taxa_prev - 0.005
    ja_virou = taxa <= CRISTA_TAXA_MIN
    if subindo and not desacelera:                       # sobe forte/acelerando -> ainda não
        return None

    ch = _chuva_driver_recente(caminho, agora, 2.0)
    chuva_parou = (ch is not None and ch <= CRISTA_CHUVA_MAX)
    if not chuva_parou:
        return None

    lideres = {nome: _lider_cristou(caminho, c, agora) for c, nome in CRISTA_LIDERES.items()}
    viradas = [nome for nome, v in lideres.items() if v is True]
    medidas = [nome for nome, v in lideres.items() if v is not None]
    if medidas and len(viradas) < max(1, len(medidas) - 1):   # maioria das medidas deve ter virado
        return None
    conf_lideres = bool(viradas)

    pico_proj, t_pico = estimador.projetar_crista_pos_chuva(niv, max(taxa, 0.0))
    pico_obs = max(v for _, v in h[-6:])                 # já pode ter passado a crista
    pico = round(max(pico_proj, pico_obs), 2)
    return {
        "ativo": True, "pico": pico, "t_ate_crista_h": round(t_pico, 1),
        "taxa_atual": round(taxa, 3), "taxa_anterior": round(taxa_prev, 3),
        "ja_virou": ja_virou, "chuva_driver_2h": (round(ch, 1) if ch is not None else None),
        "lideres_viradas": viradas, "conf_lideres": conf_lideres,
        "lideres_status": {n: ("virou" if v else ("subindo" if v is False else "sem dado"))
                           for n, v in lideres.items()},
        "teto_v1_0": teto_v1_0, "faixa": faixa_rds(pico),
    }


def estimar(raw, dams, base, t_vale, agora):
    """Roda o estimador v1.0 (OFICIAL, decide o alerta) com as grandezas do ATO, a
    SOMBRA com laterais (cj_lat) e, para comparação, o v0.9 conservador (modelo
    antigo, sem crédito de retenção). Retorna dict ou None."""
    if not TEM_MODELO or base is None or t_vale is None:
        return None
    try:
        leit, metodo_cj, cob = _leituras_ato(raw, t_vale, agora)
        chuvas_v07, chuvas_lat = fus.dicts_para_estimador(leit)
        duplo = fus.cj_duplo(leit)
        bars = barragens_ato(os.path.join(DADOS, "barragens.csv"), dams, t_vale, agora)
        dv = sum(b["dv_hm3"] for b in bars)
        fr = [b["fracao_aberta"] for b in bars if b["fracao_aberta"] is not None]
        fracao = round(sum(fr) / len(fr), 2) if fr else None
        vertendo = any(b["vertendo"] for b in bars)

        cj, fonte_cj = estimador.cj_representativa(chuvas_v07)
        acima = estimador._media(chuvas_v07, estimador.ACIMA) or 0.0
        e_of = estimador.estimar_pico(base, cj, acima, fracao, dv, vertendo, rede_completa=True)
        cj_lat = estimador._media(chuvas_lat, estimador.DRIVERS) or cj
        e_sh = estimador.estimar_pico(base, cj_lat, acima, fracao, dv, vertendo, rede_completa=True)

        antigo = None
        if estimador_v09 is not None:
            try:
                bv = [estimador_v09.BarragemV5(b["nome"], 0.0, 0.0, ocupacao_pct=b["pct_agora"],
                                               extravasor_m=(0.01 if b["vertendo"] else 0.0)) for b in bars]
                a = estimador_v09.estimar_pico_v5(base, chuvas_v07, bv, usar_ancoras=False)
                antigo = {"pico": round(a.pico_central, 1), "faixa": a.faixa}
            except Exception as ex:
                print(f"AVISO v0.9 sombra: {ex}", file=sys.stderr)

        return {
            "baseline": base, "t_vale": t_vale,
            "oficial": _resumo_v1(e_of),
            "sombra": {"pico": round(e_sh.pico_central, 1), "cj": round(cj_lat, 0)},
            "antigo_v09": antigo,
            "cj": round(cj, 1), "fonte_cj": fonte_cj, "acima": round(acima, 1),
            "metodo_cj": metodo_cj, "cobertura": cob,
            "duplo": duplo, "chuvas_v07": chuvas_v07, "bars": bars,
            "dv_hm3": round(dv, 1), "fracao_aberta": fracao, "vertendo": vertendo,
            "classe_alerta": e_of.faixa,
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

    # --- NÍVEL DE REFERÊNCIA: DC-RS Ponte Dom Tito (Asthon); SDC em paralelo ---
    live = asthon_estacoes_live()
    dom_live = live.get(DOMTITO_UUID, {}).get("level")
    dom_hist = asthon_nivel_hist(DOMTITO_UUID, VALE_MAX_H)
    sdc_niv = raw.get("00013", {}).get("nivel")
    sdc_tend = raw.get("00013", {}).get("tend")
    try:
        sdc_hist = historico_sdc(VALE_MAX_H)
    except Exception as e:
        sdc_hist = []; erros.append(f"histórico SDC: {e}")
    base_sdc = round(min(v for _, v in sdc_hist[-48:]), 2) if sdc_hist else None   # legado (mín 48h)
    off_fb = offset_fallback(os.path.join(DADOS, "nivel_rds.csv"))
    ref = resolver_referencia(sdc_niv, sdc_tend, base_sdc, dom_live, dom_hist, off_fb)

    # --- VALE DO ATO (baseline do v1.0): na régua de referência; fallback SDC+offset ---
    agora_naive = agora.replace(tzinfo=None)
    vale = detectar_vale(dom_hist) if (REFERENCIA_NIVEL == "DC_RS" and dom_hist) else None
    vale_fonte = "DC-RS"
    if vale is None and sdc_hist:
        v = detectar_vale(sdc_hist)
        if v is not None:
            vale = (v[0], round(v[1] + (off_fb if REFERENCIA_NIVEL == "DC_RS" else 0.0), 2))
            vale_fonte = f"SDC{'+offset' if REFERENCIA_NIVEL == 'DC_RS' else ''}"
    if vale is not None:
        t_vale, base_vale = vale
        ref["baseline"] = base_vale
        ref["t_vale"] = t_vale
    else:
        t_vale = agora_naive - timedelta(hours=48)     # sem série: mantém 'mín 48h' antigo
        ref["t_vale"] = None
        vale_fonte = "indisponível (baseline = mín 48h)"

    niv = ref["nivel"]; faixa = faixa_rds(niv); subindo = ref["subindo"]

    # log paralelo das DUAS réguas + offset medido (dados/nivel_rds.csv)
    _append(os.path.join(DADOS, "nivel_rds.csv"),
            ["coleta_local", "dc_rs_m", "sdc_00013_m", "offset_medido_m", "fonte", "obs"],
            [[ts, ref["dc_rs"], ref["sdc"], ref["offset_medido"], ref["fonte"], ref["obs"]]])

    # Kanitz — CHECAGEM (datum NÃO calibrado; não entra no cj/estimador)
    kz = live.get(KANITZ_UUID, {})
    kz_niv, kz_em = kz.get("level"), kz.get("em")
    kpath = os.path.join(DADOS, "kanitz.csv")
    kz_ult = _ultima_linha(kpath)
    kz_congelado = bool(kz_em and kz_ult and kz_ult.get("medida_em") == kz_em)
    if kz_niv is not None:
        _append(kpath, ["coleta_local", "medida_em", "nivel_m_raw", "fonte", "obs"],
                [[ts, kz_em, kz_niv, "Asthon Ponte Ricardo Kanitz",
                  "possível congelamento (medida_em inalterada)" if kz_congelado else ""]])

    # chuva 24h máx entre os municípios-driver (dado cru, p/ responsividade)
    driver_codes = []
    if TEM_MODELO:
        for muni, (papel, cods) in fus.MAPA_CJ.items():
            if papel in ("ancora", "driver"):
                driver_codes += cods
    ch24max = max([raw.get(c, {}).get("ch24h") or 0 for c in driver_codes] or [0])
    vertendo = any((x.get("percent_use") or 0) >= 100 or x.get("vertido") for x in dams)

    # --- ESTIMADOR v1.0 na régua de referência (+ leitura na outra régua p/ comparação) ---
    base_ref = ref["baseline"]
    est = estimar(raw, dams, base_ref, t_vale, agora_naive)
    if REFERENCIA_NIVEL == "DC_RS":
        est_dcrs = est
        base_alt = round(base_ref - off_fb, 2) if base_ref is not None else None   # em SDC
        est_sdc = estimar(raw, dams, base_alt, t_vale, agora_naive)
        base_sdc_lin, base_dcrs_lin = base_alt, base_ref
    else:
        est_sdc = est
        base_alt = round(base_ref + off_fb, 2) if base_ref is not None else None   # em DC-RS
        est_dcrs = estimar(raw, dams, base_alt, t_vale, agora_naive)
        base_sdc_lin, base_dcrs_lin = base_ref, base_alt
    stale = _stale(raw) if (TEM_MODELO and raw) else []

    # --- MODO CRISTA: nowcast na fase final (chuva encerrada, réguas-líder viradas) ---
    ref_hist = dom_hist if (REFERENCIA_NIVEL == "DC_RS" and dom_hist) else sdc_hist
    crista = modo_crista(ref_hist, os.path.join(DADOS, "serie_bacia.csv"), niv, agora_naive,
                         teto_v1_0=(est["oficial"]["pico"] if est else None))

    # Classe que dispara o alerta:
    #  - regime normal: pico central do v1.0 (OFICIAL, cj sem laterais);
    #  - MODO CRISTA ativo: a projeção da trajetória (nowcast mais preciso perto da
    #    crista; o v1.0 vira teto), nunca ABAIXO da faixa atual do rio.
    # O gatilho de EVENTO nunca é rebaixado (OU com a faixa atual e com a previsão v1.0).
    if crista:
        classe_alerta = _mais_severa(faixa if faixa != "?" else "Normal", crista["faixa"])
        crista["classe_alerta"] = classe_alerta
    else:
        classe_alerta = est["classe_alerta"] if est else faixa
    evento = (_e_alerta(faixa)
              or (subindo and ch24max >= 30) or ch24max >= 50
              or _e_alerta(classe_alerta)
              or (est is not None and _e_alerta(est["classe_alerta"])))

    # --- estado_atual.md ---
    md = [f"# Cheia — Rio do Sul (SC) — {ts} (local −03)", ""]
    md.append(f"**Rio do Sul ({ref['fonte']}):** {niv} m — **{faixa}** · "
              f"tendência {'subindo' if subindo else 'estável/caindo'}")
    md.append(f"- SDC-00013: {ref['sdc']} m · DC-RS Dom Tito: {ref['dc_rs']} m · "
              f"offset medido DC-RS−SDC: {ref['offset_medido']} m"
              + (f" · ⚠ {ref['obs']}" if ref["obs"] else ""))
    md.append(f"**Chuva 24h máx (drivers):** {round(ch24max,1)} mm")
    md.append(f"**EVENTO ATIVO:** {'🔴 SIM' if evento else '🟢 não'}")
    if crista:
        cr = crista
        st = " · ".join(f"{n}: {v}" for n, v in cr["lideres_status"].items())
        md.append("")
        md.append(f"**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** "
                  f"pico ~{cr['pico']} m → **{cr['faixa']}**"
                  + (" · crista já atingida/passando" if cr["ja_virou"]
                     else f" · crista em ~{cr['t_ate_crista_h']:.0f} h"))
        md.append(f"- método: projeção da trajetória (decaimento linear da taxa, "
                  f"validado −0,03/+0,02 nos ev.15/16). Taxa atual {cr['taxa_atual']} m/h "
                  f"(anterior {cr['taxa_anterior']} m/h) · chuva-driver 2h "
                  f"{cr['chuva_driver_2h']} mm/h")
        md.append(f"- réguas-líder: {st}"
                  + ("" if cr["conf_lideres"] else " · ⚠ sem confirmação de régua-líder"))
        if cr.get("teto_v1_0") is not None:
            md.append(f"- o v1.0 vira **TETO** (~{cr['teto_v1_0']} m); o número acima é o "
                      f"nowcast e DECIDE o alerta.")
    if evento and est:
        of = est["oficial"]; s = est["sombra"]; dpl = est["duplo"]; t = of["termos"]
        flo, fhi = of["banda"]
        tv = est["t_vale"]
        md.append("")
        rotulo = "v1.0 (TETO — modo crista ativo)" if crista else "v1.0, OFICIAL"
        md.append(f"**Pico estimado ({rotulo}):** ~{of['pico']} m "
                  f"(banda p10–p90 {flo}–{fhi} m) → **{of['faixa']}**")
        md.append(f"**Classe que dispara o alerta/e-mail: {classe_alerta}**")
        md.append(f"- baseline = VALE do ato: {est['baseline']} m em "
                  f"{tv:%d/%m %H:%M} ({vale_fonte}) · subida até agora "
                  f"{round(niv - est['baseline'], 2) if (niv is not None and est['baseline'] is not None) else '?'} m")
        md.append(f"- chuva-jusante do ato: {est['cj']} mm ({est['fonte_cj']}; {est['metodo_cj']}) · "
                  f"chuva-acima {est['acima']} mm")
        md.append(f"- cj efetiva {of['cj_ef']:.0f} mm = cj {t['cj']:.0f} + trânsito-acima "
                  f"{t['transito_acima']:.0f} (fração de comportas aberta {t['fracao_aberta']:.2f}) "
                  f"+ pluviômetro-ΔV {t['pluviometro_dv']:.0f} (ΔV do ato {est['dv_hm3']} hm³)"
                  + (" · **VERTENDO** (+%.2f m)" % estimador.V_VERT if est["vertendo"] else ""))
        md.append(f"- sombra (cj_lat, c/ laterais): ~{s['pico']} m "
                  f"(cj {s['cj']:.0f} mm · Δcj_lat−cj_v07 = "
                  f"{dpl.get('delta')} mm, n_laterais={dpl.get('n_lat_validas')})")
        if est.get("antigo_v09"):
            md.append(f"- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): "
                      f"~{est['antigo_v09']['pico']} m → {est['antigo_v09']['faixa']} (só comparação)")
        md += ["", "### Barragens no ato (desde o vale)", "",
               "| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |",
               "|---|---|---|---|---|---|---|"]
        for b in est["bars"]:
            fa = "—" if b["fracao_aberta"] is None else f"{b['fracao_aberta']:.2f}"
            md.append(f"| {b['nome']} | {b['pct_vale']} → {b['pct_agora']} | {b['dv_hm3']} | {fa} | "
                      f"{b['comportas']} | {b['montante']} m | {b['obs'] or ('vertendo' if b['vertendo'] else '')} |")
    if est and est.get("chuvas_v07"):
        cv = est["chuvas_v07"]
        drv = {k: v for k, v in cv.items() if k in getattr(estimador, "DRIVERS", [])}
        aci = {k: v for k, v in cv.items() if k in getattr(estimador, "ACIMA", [])}
        md += ["", f"## Chuva-jusante fundida DO ATO — {est['metodo_cj']}",
               "", "| Município | Chuva do ato (mm) |", "|---|---|"]
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
    # --- Fase 5: comparação de datum A(SDC) vs B(DC-RS) ---
    def _lin(e, base_):
        if not e:
            return f"baseline {base_} m · (estimador indisponível)"
        fpk = e["oficial"]["pico"]; flo, fhi = e["oficial"]["banda"]
        return (f"baseline {base_} m · pico v1.0 ~{fpk} m (banda {flo}–{fhi}) "
                f"→ **{e['oficial']['faixa']}**")
    md += ["", "## Referência de nível — DC-RS Dom Tito (troca de datum)", "",
           f"Referência ATIVA: **{ref['fonte']}** · offset medido DC-RS−SDC: "
           f"**{ref['offset_medido']} m** · fallback {off_fb} m",
           f"- **A) SDC-00013:** " + _lin(est_sdc, base_sdc_lin),
           f"- **B) DC-RS Dom Tito:** " + _lin(est_dcrs, base_dcrs_lin)]
    if est_dcrs and est_sdc:
        dpk = est_dcrs["oficial"]["pico"] - est_sdc["oficial"]["pico"]
        mud = est_dcrs["oficial"]["faixa"] != est_sdc["oficial"]["faixa"]
        md.append(f"- **Δ pico (B − A): {dpk:+.2f} m**"
                  + (f" · ⚠ MUDA A CLASSE: {est_sdc['oficial']['faixa']} → "
                     f"{est_dcrs['oficial']['faixa']}" if mud else " · classe inalterada"))
    md.append(f"- nível atual: SDC {ref['sdc']} m · DC-RS {ref['dc_rs']} m"
              + (f" · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): {kz_niv} m"
                 if kz_niv is not None else ""))

    avisos = list(erros)
    if "indisponível" in ref["fonte"]:
        avisos.append(ref["obs"])
    if kz_congelado:
        avisos.append("Kanitz possivelmente congelada (medida_em inalterada) — só checagem")
    if stale:
        avisos.append("Sensores TRAVADOS (descartados na fusão): " + ", ".join(stale))
    if avisos:
        md += ["", "## ⚠ Avisos desta coleta", ""] + [f"- {a}" for a in avisos]
    with open("estado_atual.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    with open("evento.txt", "w", encoding="utf-8") as f:
        f.write("SIM" if evento else "NAO")

    pico_fino = est["oficial"]["pico"] if est else None
    pico_msg = crista["pico"] if crista else pico_fino
    assunto = (f"[CHEIA {classe_alerta}] Rio do Sul {niv} m"
               + (f" · pico~{pico_msg} m" + (" (crista)" if crista else "")
                  if evento and pico_msg is not None else "")) if evento \
              else f"[ok] Rio do Sul normal — {niv} m"
    with open("assunto.txt", "w", encoding="utf-8") as f:
        f.write(assunto)

    crista_msg = ""
    if crista:
        quando = "passou" if crista["ja_virou"] else f"+{crista['t_ate_crista_h']:.0f}h"
        crista_msg = f" | MODO CRISTA ~{crista['pico']} m ({quando})"
    print(f"EVENTO={'SIM' if evento else 'NAO'} | Rio do Sul {niv} m [{faixa}] "
          f"| chuva24h máx {round(ch24max,1)} mm"
          + (f" | v1.0 ~{pico_fino} m (banda {est['oficial']['banda'][0]}–{est['oficial']['banda'][1]}) "
             f"vale {est['baseline']} m @ {est['t_vale']:%d/%m %H:%M} · cj {est['cj']} mm · "
             f"ΔV {est['dv_hm3']} hm³" if est else "")
          + crista_msg
          + (f" [alerta {classe_alerta}]" if est or crista else ""))
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
