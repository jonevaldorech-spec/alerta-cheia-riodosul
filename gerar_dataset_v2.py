# -*- coding: utf-8 -*-
"""gerar_dataset_v2.py — dataset por ato com features de BARRAGEM (v2, 06/09/2026;
apontado para v24/v1_7 em 07/09/2026).
Lê Enchentes_Consolidado_v24.xlsx (abas de barragens de todas as épocas — idênticas
às da v23) + dataset_ml_v1_7.csv (usa só as 31 colunas-base do evento; as demais 49
são features/erros já derivados e são recalculados aqui)
e calcula, por ato, com as curvas V(h) v0.7 (ou % oficial quando existe):
  *_pct_ini / *_pct_pk8 / *_pct_pk  ocupação (%) no início do ato, em t_pico−8h e no pico
  *_dv8 / *_dv12 / *_dv24 / *_dv_ev  volume retido (hm³) nas janelas 8/12/24 h e no ATO inteiro
  *_ffech_ev / _8h / _24h            fração de comportas FECHADAS ponderada no tempo
  pct_max_max, verteu_flag           ocupação máxima e vertimento
Saída: dataset_eventos_v2.csv (na pasta do projeto). Uso: python gerar_dataset_v2.py
"""
import re, csv, os, sys, tempfile
import numpy as np, pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook

PROJ = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(PROJ, "Enchentes_Consolidado_v24.xlsx")
BASE_ML = os.path.join(PROJ, "dataset_ml_v1_7.csv")   # base de eventos (31 col. iniciais)
# 31 colunas-base do ato (= dataset_ml_v1_6); as demais colunas do v1_7 são features
# de barragem/erros já derivadas e são RECALCULADAS por este script — não relê-las.
BASE_COLS = ['evento', 'ano', 'inicio', 'pico_dt', 'antec_h', 'nivel_inicial',
             'nivel_pico', 'elevacao', 'chuva_rsul', 'chuva_itu', 'chuva_taio',
             'cj_ancoras', 'cj_jusante', 'chuva_acima', 'sens_catalogo',
             'barr_oeste_pct_ini', 'barr_sul_pct_ini', 'estado_barragens', 'verteu',
             'epoca_offset_dcrs_sdc', 'epoca_rede', 'em_dominio_v06',
             'motivo_fora_dominio', 'flag_janela_fixa', 'usar_para_calibracao',
             'lat_atalanta', 'lat_petrolandia', 'lat_mirim_doce', 'lat_braco_trombudo',
             'laterais_no_cj', 'obs_laterais']
ABAS = os.path.join(tempfile.gettempdir(), "abas_enchentes_v24")
OUT = os.path.join(PROJ, "dataset_eventos_v2.csv")
os.makedirs(ABAS, exist_ok=True)
_wb = load_workbook(XLSX, read_only=True, data_only=True)
for _ws in _wb.worksheets:
    _n = "".join(c if c.isalnum() else "_" for c in _ws.title)
    with open(os.path.join(ABAS, _n + ".csv"), "w", newline="", encoding="utf-8") as _f:
        _w = csv.writer(_f)
        for _r in _ws.iter_rows(values_only=True):
            _w.writerow(["" if v is None else v for v in _r])
VH = {"Sul": dict(h0=6.85, c=0.05000, p=2.399, vt=104.03),
      "Oeste": dict(h0=7.55, c=2.00372, p=1.419, vt=99.96)}
NCOMP = {"Sul": 5, "Oeste": 7}

def vol(b, h):
    k = VH[b]; x = max(0.0, h - k["h0"]); return k["c"] * x ** k["p"]
def pct_curva(b, h): return 100 * vol(b, h) / VH[b]["vt"]

def num(x):
    if x is None: return np.nan
    s = str(x).strip().replace(",", ".")
    if s in ("", "-", "—", "nan", "None"): return np.nan
    try: return float(s)
    except ValueError: return np.nan

rows = []  # (barragem, dt, montante, pct_of, abertas, fechadas, fonte)
def add(b, dt, m, pct, a, f, fonte):
    if pd.isna(dt): return
    rows.append(dict(barragem=b, dt=dt, montante=num(m), pct_of=num(pct),
                     abertas=num(a), fechadas=num(f), fonte=fonte))

def rd(name):
    return list(csv.reader(open(os.path.join(ABAS, name), encoding="utf-8")))

# 1. 2023 boletins 3h
for r in rd("Barragens_2023__Boletins_.csv")[2:]:
    if not r or not r[0].startswith("2023"): continue
    dt = pd.Timestamp(r[0])
    add("Sul", dt, r[1], r[6], r[2], r[3], "bol2023")
    add("Oeste", dt, r[7], r[12], r[8], r[9], "bol2023")
# erro conhecido: 27/11 07h duplicata do 28/11 07h -> remove
rows = [x for x in rows if not (x["fonte"] == "bol2023" and x["dt"] == pd.Timestamp("2023-11-27 07:00"))]
# 2. Jul23
for r in rd("EvJul23_Barragens__boletins_.csv")[1:]:
    if not r or not r[0].startswith("2023-07"): continue
    dt = pd.Timestamp(r[0])
    add("Sul", dt, r[2], r[7], r[4], r[5], "bolJul23")
    add("Oeste", dt, r[8], r[13], r[10], r[11], "bolJul23")
# 3. 2024 SPDC (Oeste % congelada -> ignora %)
for r in rd("Barragens_2024__SPDC_.csv")[3:]:
    if not r or not r[0].startswith("2024"): continue
    dt = pd.Timestamp(r[0])
    m_sul = num(r[1]); m_oes = num(r[7])
    if m_sul > 100: m_sul = np.nan   # 250 = erro de digitação
    add("Sul", dt, m_sul, r[5], r[3], r[4], "spdc2024")
    add("Oeste", dt, m_oes, None, r[9], r[10], "spdc2024")
# 4. I2 (2 fontes) — já coberto pelo SPDC; usa % DC-RO da Oeste
for r in rd("EvI2_Barragens__2_fontes_.csv")[2:]:
    if len(r) < 7 or not r[1].startswith("2024"): continue
    if r[0] == "Oeste":
        add("Oeste", pd.Timestamp(r[1]), r[2], r[6], r[4], r[5], "dcro2024")
# 5. Ev14 (painel DC-RS 2026)
blk = None
for r in rd("Ev14_Barragens__DC_RS_.csv"):
    if r and r[0].startswith("BARRAGEM SUL"): blk = "Sul"; continue
    if r and r[0].startswith("BARRAGEM OESTE"): blk = "Oeste"; continue
    if blk and r and re.match(r"\d\d/\d\d \d\dH", r[0]):
        d, h = r[0].split(); dt = pd.Timestamp(f"2026-{d[3:5]}-{d[0:2]} {h[:2]}:00")
        add(blk, dt, r[1], None, r[4], r[5], "painel2026")
# 6. Ev15
for r in rd("Ev15_Barragens__painel_.csv")[3:]:
    if len(r) < 6 or r[0] not in ("Sul", "Oeste"): continue
    d = r[1]; h = r[2]; dt = pd.Timestamp(f"2026-{d[3:5]}-{d[0:2]} {h[:2]}:00")
    add(r[0], dt, r[3], r[6] if len(r) > 6 else None, r[4], r[5], "painel2026")
# 7. Ev16 (registro oficial + % CSV)
sec = None
pct16 = {}
for r in rd("Ev16_Barragens__oficial_.csv"):
    if r and r[0].startswith("REGISTRO OFICIAL"): sec = "reg"; continue
    if r and r[0].startswith("OCUPAÇÃO"): sec = "pct"; continue
    if r and r[0].startswith("VALIDAÇÃO"): sec = None; continue
    if sec == "reg" and r and r[0] in ("SUL", "OESTE") and re.match(r"\d\d/\d\d \d\dH", r[1]):
        d, h = r[1].split(); dt = pd.Timestamp(f"2026-{d[3:5]}-{d[0:2]} {h[:2]}:00")
        add(r[0].title(), dt, r[2], None, r[4], r[5], "painel2026")
    if sec == "pct" and r and r[0] in ("SUL", "OESTE") and re.match(r"\d\d/\d\d/\d{4}", r[1]):
        dt = pd.Timestamp(datetime.strptime(r[1], "%d/%m/%Y %H:%M"))
        pct16[(r[0].title(), dt)] = num(r[2])
for x in rows:
    if x["fonte"] == "painel2026" and (x["barragem"], x["dt"]) in pct16:
        x["pct_of"] = pct16[(x["barragem"], x["dt"])]
# 8. Ev17 Asthon horário
for r in rd("Ev17_Barragens__Asthon_.csv")[5:]:
    if len(r) < 6 or not r[0].startswith("2026"): continue
    b = "Sul" if "Sul" in r[1] else "Oeste"
    mm = re.match(r"(\d+)A/(\d+)F", r[3])
    a, f = (mm.group(1), mm.group(2)) if mm else (None, None)
    add(b, pd.Timestamp(r[0]), r[5], r[2], a, f, "asthon2026")
# 9. 2025 boletins
for r in rd("Ev2025_Barragens__DC_RS_.csv")[1:]:
    if len(r) < 6 or not re.match(r"\d\d/\d\d/2025", r[1]): continue
    b = "Sul" if r[0].startswith("Sul") else "Oeste"
    dt = pd.Timestamp(datetime.strptime(r[1], "%d/%m/%Y %Hh"))
    add(b, dt, r[2], None, r[4], r[5], "bol2025")
# 10. 2022 boletins
for r in rd("Ev2022_Barragens__DC_RS_.csv")[1:]:
    if len(r) < 6 or not re.match(r"\d\d/\d\d/2022", r[1]): continue
    b = "Sul" if r[0].upper().startswith("SUL") else "Oeste"
    dt = pd.Timestamp(datetime.strptime(r[1], "%d/%m/%Y %Hh%M"))
    add(b, dt, r[2], None, r[4], r[5], "bol2022")
# 11. 2021 / 2020 boletins (ISO)
for fn, fonte in (("Ev2021_Barragens__DC_RS_.csv", "bol2021"), ("Ev2020_Barragens__DC_RS_.csv", "bol2020")):
    for r in rd(fn)[2:]:
        if len(r) < 6 or not re.match(r"20\d\d-", r[1]): continue
        b = "Sul" if r[0].upper().startswith("SUL") else "Oeste"
        m = num(r[2])
        if fonte == "bol2020" and b == "Oeste" and r[1].startswith("2020-08-16 11"): m = np.nan  # digitação
        add(b, pd.Timestamp(r[1]), m, None, r[4], r[5], fonte)
# 12. 2018 boletins
for r in rd("Ev2018_Barragens__DC_RS_.csv")[3:]:
    if len(r) < 6 or not re.match(r"2018-", r[1]): continue
    add(r[0], pd.Timestamp(r[1]), r[2], None, r[4], r[5], "bol2018")
# 12b. Dez/2023 — ficha da Base de Eventos (sem boletim): leituras aproximadas 07/12 16h -> 08/12 07h
for dt, ms, mo, fs, fo in (("2023-12-07 07:00", 25.58, 15.61, 2, 4), ("2023-12-07 17:00", 25.60, 15.50, 2, 4), ("2023-12-08 07:00", 25.63, 15.20, 2, 2)):
    add("Sul", pd.Timestamp(dt), ms, None, 5-fs, fs, "fichaDez23"); add("Oeste", pd.Timestamp(dt), mo, None, 7-fo, fo, "fichaDez23")
# 13. 2017 (só montante)
for r in rd("Ev_MaiJun17_Barragens__mont__.csv")[1:]:
    if len(r) < 3 or not re.match(r"2017-", r[1]): continue
    b = "Sul" if r[0].startswith("Sul") else "Oeste"
    add(b, pd.Timestamp(r[1]), r[2], None, None, None, "bol2017")

S = pd.DataFrame(rows).dropna(subset=["dt"]).sort_values(["barragem", "dt"])
S = S.drop_duplicates(["barragem", "dt", "fonte"])
S["pct_curva"] = [pct_curva(b, m) if pd.notna(m) else np.nan for b, m in zip(S.barragem, S.montante)]
# ocupação de trabalho: % oficial quando existe (fonte confiável), senão curva
S["pct"] = S.pct_of.where(S.pct_of.notna(), S.pct_curva)
S["vol"] = S.pct / 100 * S.barragem.map({k: v["vt"] for k, v in VH.items()})
S.to_csv(os.path.join(PROJ, "serie_barragens_long_v2.csv"), index=False)
print("série longa:", len(S), "linhas;", S.groupby("fonte").size().to_dict())

# ---------------------------------------------------------------- eventos
D = pd.read_csv(BASE_ML, usecols=lambda c: c in BASE_COLS)[BASE_COLS]
D["inicio"] = pd.to_datetime(D.inicio, format="mixed"); D["pico_dt"] = pd.to_datetime(D.pico_dt, format="mixed")

def interp(ser, t):
    """interpola linearmente ser (index dt) em t; NaN se fora da faixa >12h"""
    ser = ser.dropna()
    if ser.empty: return np.nan
    if t < ser.index[0] - timedelta(hours=12) or t > ser.index[-1] + timedelta(hours=12): return np.nan
    if t <= ser.index[0]: return ser.iloc[0]
    if t >= ser.index[-1]: return ser.iloc[-1]
    i = ser.index.searchsorted(t)
    t0, t1 = ser.index[i-1], ser.index[i]
    w = (t - t0) / (t1 - t0)
    return ser.iloc[i-1] * (1 - w) + ser.iloc[i] * w

def frac_fechada(sub, t0, t1):
    """fração de comportas fechadas ponderada no tempo em [t0,t1] (step function)"""
    sub = sub.dropna(subset=["fechadas"]).sort_values("dt")
    if sub.empty: return np.nan
    tot = 0.0; acc = 0.0
    times = list(sub.dt); vals = list(sub.fechadas / sub.barragem.map(NCOMP))
    # estado antes da primeira leitura = primeira leitura
    t = t0
    while t < t1:
        i = max(0, np.searchsorted(np.array(times, dtype="datetime64[ns]"), np.datetime64(t), side="right") - 1)
        # próximo passo
        nxt = times[i+1] if i + 1 < len(times) and times[i+1] > t else t1
        nxt = min(nxt, t1)
        if nxt <= t: nxt = t1
        dt_h = (nxt - t).total_seconds() / 3600
        acc += vals[i] * dt_h; tot += dt_h; t = nxt
    return acc / tot if tot > 0 else np.nan

out = []
for _, e in D.iterrows():
    rec = dict(evento=e.evento)
    tp, ti = e.pico_dt, e.inicio
    if pd.isna(tp): out.append(rec); continue
    for b in ("Sul", "Oeste"):
        sub = S[(S.barragem == b) & (S.dt >= ti - timedelta(hours=36)) & (S.dt <= tp + timedelta(hours=36))]
        k = b[0].lower()
        if sub.empty:
            rec.update({f"{k}_dv8": np.nan}); continue
        pser = sub.set_index("dt").pct
        mser = sub.set_index("dt").montante
        p_ini, p_8, p_pk = interp(pser, ti), interp(pser, tp - timedelta(hours=8)), interp(pser, tp)
        vt = VH[b]["vt"]
        rec[f"{k}_pct_ini"] = p_ini; rec[f"{k}_pct_pk8"] = p_8; rec[f"{k}_pct_pk"] = p_pk
        rec[f"{k}_dv8"] = (p_pk - p_8) / 100 * vt if pd.notna(p_pk) and pd.notna(p_8) else np.nan
        rec[f"{k}_dv_ev"] = (p_pk - p_ini) / 100 * vt if pd.notna(p_pk) and pd.notna(p_ini) else np.nan
        rec[f"{k}_dv12"] = (p_pk - interp(pser, tp - timedelta(hours=12))) / 100 * vt if pd.notna(p_pk) else np.nan
        rec[f"{k}_dv24"] = (p_pk - interp(pser, tp - timedelta(hours=24))) / 100 * vt if pd.notna(p_pk) else np.nan
        janela = sub[(sub.dt >= tp - timedelta(hours=8)) & (sub.dt <= tp + timedelta(hours=8))]
        rec[f"{k}_pct_max"] = pser[(pser.index >= ti) & (pser.index <= tp + timedelta(hours=6))].max()
        rec[f"{k}_ffech_ev"] = frac_fechada(sub, ti, tp)          # fração fechada média no ato
        rec[f"{k}_ffech_8h"] = frac_fechada(sub, tp - timedelta(hours=8), tp)
        rec[f"{k}_ffech_24h"] = frac_fechada(sub, tp - timedelta(hours=24), tp)
        # comportas no pico (último registro <= tp)
        last = sub[sub.dt <= tp].dropna(subset=["fechadas"])
        rec[f"{k}_fech_pk"] = last.fechadas.iloc[-1] if not last.empty else np.nan
        rec[f"{k}_fonte"] = sub.fonte.mode().iloc[0]
        rec[f"{k}_cad_h"] = float(np.median(np.diff(sub.dt.values).astype("timedelta64[m]").astype(float)) / 60) if len(sub) > 1 else np.nan
        rec[f"{k}_pct_oficial"] = sub.pct_of.notna().mean() > 0.5
    out.append(rec)
F = pd.DataFrame(out)
X = D.merge(F, on="evento", how="left")
for c in ("dv8", "dv12", "dv24", "dv_ev"):
    X[f"dv_{c[2:]}_tot" if c != "dv_ev" else "dv_ev_tot"] = X[[f"s_{c}", f"o_{c}"]].sum(axis=1, min_count=1)
X["pct_max_max"] = X[["s_pct_max", "o_pct_max"]].max(axis=1)
X["verteu_flag"] = X.verteu.astype(str).str.upper().str.startswith("SIM") | (X.pct_max_max >= 100)
X.to_csv(OUT, index=False, encoding="utf-8-sig")
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
cols = ["evento", "nivel_inicial", "nivel_pico", "cj_jusante", "chuva_acima", "s_pct_ini", "s_pct_pk", "o_pct_ini", "o_pct_pk",
        "s_dv8", "o_dv8", "dv_8_tot", "dv_ev_tot", "s_ffech_ev", "o_ffech_ev", "s_ffech_8h", "o_ffech_8h", "pct_max_max", "verteu_flag", "s_fonte", "s_cad_h"]
print(X[cols].round(2).to_string())
