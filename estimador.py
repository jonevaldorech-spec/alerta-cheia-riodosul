# -*- coding: utf-8 -*-
"""
ESTIMADOR DE PICO v1.0 — Rio do Sul (Itajaí-Açu) — 06/09/2026
==============================================================
Reformulação calibrada em TODOS os atos do catálogo com dado de barragem
(43 atos, 2018–2026; dataset_eventos_v2.csv), validada por leave-one-flood-out
(LOO) e leave-one-year-out (LOYO). Substitui a linhagem v0.5–v0.10 na operação.

O QUE MUDA EM RELAÇÃO AO v0.10 (e por quê)
------------------------------------------
1. NÃO há mais "termo volumétrico" (−ΔV/DQDH). Ajustado sobre 43 atos, o
   coeficiente do ΔV da janela [t_pico−8h, t_pico] converge a ZERO em todas as
   formulações testadas (janelas 8/12/24 h). O que a montante mede não é o
   corte do pico: o efeito de retenção já está embutido em usar só a chuva
   JUSANTE (cj) como driver. Teste pré-registrado de DQDH (300/400/535/700/1000)
   na réplica do v0.9: quanto MENOR o DQDH (termo maior), PIOR o RMSE.
2. O ENCHIMENTO TOTAL das barragens no ato (ΔV_evento = V(t_pico) − V(vale))
   entra com sinal POSITIVO, como medida independente de chuva ("reservatório
   como pluviômetro", Achado 2 do próprio projeto, Instruções v26 §D2). Reduz o
   LOO de 0,57 → 0,45 m nos 18 calibráveis e 0,80 → 0,71 m nos 43 atos.
3. Curva côncava SUAVE: s(h) = s0·exp(−b·h) m/100 mm, integrada em forma
   fechada (sem zonas com degrau). Com os parâmetros ajustados:
   h=2 → 3,8 · h=4 → 3,2 · h=6 → 2,7 · h=8 → 2,3 · h=10 → 1,9 m/100 mm.
4. Gate-state mantido: a chuva-ACIMA transita ponderada pela fração de
   comportas ABERTAS no ato (k ≈ 0,42; era 0,35 fixo). Com comportas fechadas
   a chuva-acima NÃO entra (o que estava certo no fix v0.10) — mas o v0.10
   sozinho, sem o termo do item 2, subestima em −0,41 m (viés medido nos 18
   calibráveis). O item 2 é o que faltava.
5. Vertimento: +0,37 m (flag), não +1,0. Excedência em lâmina testada, não
   melhora (n=9 vertimentos).
6. BANDA a partir dos resíduos LOO reais (p10/p90 por classe), não de
   "±30 % do termo".

RESULTADO (erro = previsto − observado, m; LOO = fora da amostra por ato)
  18 atos calibráveis:  LOO RMSE 0,39 (ajuste com os 43) / 0,45 (ajuste só com os 18) · viés +0,05
  43 atos (2018–2026):  LOO RMSE 0,71 · viés −0,07 · LOYO 0,76
  Referência v0.9 (réplica, mesmos inputs): 0,45 (18, em amostra) / 0,93 (43)
  Referência v0.10 gate-state:              0,75 / 1,10 (viés −0,41 / −0,45)
  Sem os 5 atos com chuva sabidamente submedida (A, H, Jun22, Jun21, Set21):
  LOO RMSE 0,44 em 38 atos.
  Resíduos grandes remanescentes: A −2,0 · H −1,6 · Jun22 −1,7 · Set21 −1,6 ·
  Jun21 −1,1 (todos com chuva submedida, já sinalizados no catálogo).

INPUTS (todos observáveis ao vivo)
  nivel_inicial   baseline DC-RS do ato (vale pré-evento ou trough J2) [m]
  cj              chuva-JUSANTE representativa do ato (soma horária na janela
                  vale → agora/pico; NUNCA o acumulado rolante 48 h) [mm]
  chuva_acima     média das estações ACIMA das barragens na mesma janela [mm]
  fracao_aberta   fração média de comportas ABERTAS durante o ato (0..1),
                  média das duas barragens ponderada no tempo; None → 0,5
  dv_evento_hm3   Σ [V(agora) − V(vale)] das duas barragens [hm³], via % de
                  ocupação (painel/Asthon/CSV 00038-00040) ou montante→V(h) v0.7
  vertendo        True se alguma barragem ≥100 % ou extravasor > 0

USO
  from estimador_pico_v1_0 import estimar_pico
  e = estimar_pico(3.26, cj=94.6, chuva_acima=73.7, fracao_aberta=0.0,
                   dv_evento_hm3=62.9, vertendo=False)      # Set26 → ~7,0 (obs 6,78)
  print(e)

Compatibilidade: estimar_pico_v5(nivel_inicial, chuvas_mm, barragens) aceita
os mesmos objetos BarragemV5 do v0.10 (montante_inicio/fim, ocupacao_pct,
fracao_aberta_chuva) — mas ATENÇÃO: nessa API montante_inicio deve ser a
montante no VALE do ato (não t_pico−8h), porque o termo agora é ΔV do ATO.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable
import math

# ----------------------------------------------------------------------
# 0. PARÂMETROS (ajuste robusto soft-L1, pesos 1,0 calibráveis / 0,5 demais,
#    43 atos; LOO/LOYO em Analise_Estimador_v1_0.md)
# ----------------------------------------------------------------------
S0 = 4.5886        # m/100 mm — sensibilidade em h = 0
B = 0.0886         # 1/m — decaimento da sensibilidade com o nível
K_ACIMA = 0.4182   # fração da chuva-acima que transita POR COMPORTA ABERTA
M_DV = 0.7096      # mm de chuva-equivalente por hm³ retido no ato (pluviômetro)
V_VERT = 0.3746    # m — barragem vertendo (≥100 % / extravasor)
FRACAO_ABERTA_PADRAO = 0.5

# Bandas = percentis dos resíduos LOO (previsto − observado), por classe
BANDA_LOO = {   # classe: (p10, p50, p90)
    "calibravel":  (-0.50, +0.14, +0.49),   # rede SDC + % oficial (n=18)
    "geral":       (-1.00, +0.08, +0.67),   # todos os 43 atos
    "vertendo":    (-0.62, -0.02, +0.76),
    "ni_baixo":    (-1.54, -0.05, +0.65),   # nível inicial < 3 m (n=22)
    "ni_medio":    (-0.61, +0.22, +0.67),   # 3–5 m
    "ni_alto":     (-0.62, -0.02, +0.51),   # ≥ 5 m
}
RMSE_LOO = {"calibravel": 0.39, "geral": 0.71}

NIVEIS = [("Normal", 0.0), ("Atenção", 4.5), ("Alerta", 5.5), ("Emergência", 6.5)]
VOL_TOTAL = {"Sul": 104.03, "Oeste": 99.96}       # hm³ (painel, ev.14)
COMPORTAS_TOTAL = {"Sul": 5, "Oeste": 7}
# Curvas V(h) v0.7 (montante → hm³) — inalteradas
_CURVAS_VH = {"Sul": dict(h0=6.85, c=0.05000, p=2.399),
              "Oeste": dict(h0=7.55, c=2.00372, p=1.419)}


def volume_reservatorio(barragem: str, montante_m: float) -> float:
    k = _CURVAS_VH[barragem]
    return k["c"] * max(0.0, montante_m - k["h0"]) ** k["p"]

def ocupacao_de_montante(barragem: str, montante_m: float) -> float:
    return 100.0 * volume_reservatorio(barragem, montante_m) / VOL_TOTAL[barragem]

def volume_de_ocupacao(barragem: str, pct: float) -> float:
    return pct / 100.0 * VOL_TOTAL[barragem]

def classificar(nivel: float) -> str:
    faixa = "Normal"
    for nome, lim in NIVEIS:
        if nivel >= lim:
            faixa = nome
    return faixa


# ----------------------------------------------------------------------
# 1. NÚCLEO
# ----------------------------------------------------------------------
def sensibilidade(h: float) -> float:
    """m de subida por 100 mm de chuva efetiva, no nível h."""
    return S0 * math.exp(-B * h)

def nivel_apos_chuva(nivel_inicial: float, chuva_ef_mm: float) -> float:
    """Integra dh/dP = s0·e^{−b h}: h = ln(e^{b·ni} + b·s0·P)/b, P em m (mm/100)."""
    P = max(0.0, chuva_ef_mm) / 100.0
    return math.log(math.exp(B * nivel_inicial) + B * S0 * P) / B

def chuva_efetiva(cj_mm: float, chuva_acima_mm: float = 0.0,
                  fracao_aberta: Optional[float] = None,
                  dv_evento_hm3: float = 0.0) -> tuple[float, dict]:
    fa = FRACAO_ABERTA_PADRAO if fracao_aberta is None else min(1.0, max(0.0, fracao_aberta))
    t_acima = K_ACIMA * max(0.0, chuva_acima_mm) * fa
    t_dv = M_DV * max(0.0, dv_evento_hm3)
    return cj_mm + t_acima + t_dv, {"cj": cj_mm, "transito_acima": t_acima, "pluviometro_dv": t_dv,
                                    "fracao_aberta": fa}


@dataclass
class Estimativa:
    pico_central: float
    banda: tuple[float, float]
    faixa: str
    nivel_inicial: float
    cj_efetiva_mm: float
    termos: dict
    classe_banda: str
    nota: str = ""

    def __str__(self):
        lo, hi = self.banda
        t = self.termos
        return (f"PICO: {self.pico_central:.2f} m (banda p10–p90 {lo:.2f}–{hi:.2f}) -> {self.faixa}\n"
                f"  nível inicial: {self.nivel_inicial:.2f} m | cj efetiva {self.cj_efetiva_mm:.0f} mm = "
                f"cj {t['cj']:.0f} + trânsito-acima {t['transito_acima']:.0f} (fração aberta {t['fracao_aberta']:.2f}) "
                f"+ pluviômetro-ΔV {t['pluviometro_dv']:.0f}\n"
                f"  vertimento: {'+%.2f m' % V_VERT if t.get('vertendo') else 'não'} | banda classe '{self.classe_banda}'"
                + (f"\n  nota: {self.nota}" if self.nota else ""))


def _classe_banda(nivel_inicial: float, vertendo: bool, rede_completa: bool) -> str:
    if vertendo:
        return "vertendo"
    if rede_completa:
        return "calibravel"
    if nivel_inicial < 3.0:
        return "ni_baixo"
    return "ni_medio" if nivel_inicial < 5.0 else "ni_alto"


def estimar_pico(nivel_inicial: float, cj: float, chuva_acima: float = 0.0,
                 fracao_aberta: Optional[float] = None, dv_evento_hm3: float = 0.0,
                 vertendo: bool = False, rede_completa: bool = True,
                 nota: str = "") -> Estimativa:
    """Estimador v1.0. Ver docstring do módulo para a definição dos inputs."""
    cj_ef, termos = chuva_efetiva(cj, chuva_acima, fracao_aberta, dv_evento_hm3)
    termos["vertendo"] = bool(vertendo)
    pico = nivel_apos_chuva(nivel_inicial, cj_ef) + (V_VERT if vertendo else 0.0)
    classe = _classe_banda(nivel_inicial, vertendo, rede_completa)
    p10, p50, p90 = BANDA_LOO[classe]
    # banda = pico − resíduo (resíduo = previsto − observado): observado ≈ pico − e
    banda = (pico - p90, pico - p10)
    return Estimativa(pico, banda, classificar(pico), nivel_inicial, cj_ef, termos, classe, nota)


# ----------------------------------------------------------------------
# 2. UTILITÁRIOS DE BARRAGEM (montar os inputs a partir do que se observa)
# ----------------------------------------------------------------------
def fracao_aberta_media(log_comportas: Iterable[tuple], t_ini, t_fim, total: int) -> float:
    """log_comportas = [(datetime, n_abertas), ...] em ordem; devolve a fração
    ABERTA ponderada no tempo em [t_ini, t_fim] (função-degrau)."""
    log = sorted(log_comportas, key=lambda x: x[0])
    if not log:
        return FRACAO_ABERTA_PADRAO
    acc = 0.0; tot = 0.0; t = t_ini
    while t < t_fim:
        i = max(0, max((j for j, (tj, _) in enumerate(log) if tj <= t), default=0))
        nxt = log[i + 1][0] if i + 1 < len(log) and log[i + 1][0] > t else t_fim
        nxt = min(nxt, t_fim)
        h = (nxt - t).total_seconds() / 3600.0
        acc += (log[i][1] / total) * h; tot += h; t = nxt
    return acc / tot if tot > 0 else FRACAO_ABERTA_PADRAO

def dv_evento(pct_vale: dict, pct_agora: dict) -> float:
    """Σ volume retido desde o vale, pelas % de ocupação {'Sul': %, 'Oeste': %}."""
    tot = 0.0
    for b in ("Sul", "Oeste"):
        if b in pct_vale and b in pct_agora and pct_vale[b] is not None and pct_agora[b] is not None:
            tot += max(0.0, volume_de_ocupacao(b, pct_agora[b]) - volume_de_ocupacao(b, pct_vale[b]))
    return tot


# ----------------------------------------------------------------------
# 3. COMPATIBILIDADE COM A API v0.5–v0.10 (BarragemV5 / estimar_pico_v5)
# ----------------------------------------------------------------------
@dataclass
class BarragemV5:
    nome: str
    montante_inicio_m: float        # AGORA: montante no VALE do ato
    montante_fim_m: float           # montante atual / no pico
    ocupacao_pct: Optional[float] = None
    extravasor_m: float = 0.0
    fracao_aberta_chuva: Optional[float] = None
    ocupacao_inicio_pct: Optional[float] = None   # se conhecida, prevalece sobre a montante

    @property
    def ocupacao(self) -> float:
        return self.ocupacao_pct if self.ocupacao_pct is not None else ocupacao_de_montante(self.nome, self.montante_fim_m)

    @property
    def vertendo(self) -> bool:
        return self.extravasor_m > 0 or self.ocupacao >= 100.0

    @property
    def volume_retido_hm3(self) -> float:
        v_fim = volume_de_ocupacao(self.nome, self.ocupacao)
        v_ini = (volume_de_ocupacao(self.nome, self.ocupacao_inicio_pct) if self.ocupacao_inicio_pct is not None
                 else volume_reservatorio(self.nome, self.montante_inicio_m))
        return max(0.0, v_fim - v_ini)

ANCORAS = ["Rio do Sul", "Ituporanga", "Taio"]
DRIVERS = ["Rio do Sul", "Ituporanga", "Aurora", "Taio", "Salete", "Rio do Oeste", "Laurentino",
           "Pouso Redondo", "Agrolandia", "Trombudo Central", "Agronomica",
           "Petrolandia", "Atalanta", "Mirim Doce", "Braco do Trombudo"]
ACIMA = ["Rio do Campo", "Taio_montante", "Alfredo Wagner", "Chapadao do Lageado", "Imbuia"]

def _media(chuvas: dict, chaves: list) -> Optional[float]:
    v = [chuvas[c] for c in chaves if c in chuvas and chuvas[c] is not None]
    return sum(v) / len(v) if v else None

def cj_representativa(chuvas_mm: dict, limiar: float = 0.10) -> tuple[float, str]:
    anc, drv = _media(chuvas_mm, ANCORAS), _media(chuvas_mm, DRIVERS)
    if anc is None and drv is None:
        raise ValueError("Nenhuma estação de chuva-jusante no dicionário.")
    if anc is None: return drv, "drivers"
    if drv is None or (anc > 0 and abs(drv - anc) / anc <= limiar): return anc, "ancoras"
    return drv, f"drivers (divergiu {100*(drv-anc)/anc:+.0f}% das ancoras)"

def estimar_pico_v5(nivel_inicial: float, chuvas_mm: dict, barragens: list,
                    usar_ancoras: bool = True, rede_completa: bool = True) -> Estimativa:
    """Mesma assinatura do v0.10. cj = âncoras (ou drivers se usar_ancoras=False),
    com desvio automático para drivers quando divergem >10 %."""
    if usar_ancoras:
        cj, fonte = cj_representativa(chuvas_mm)
    else:
        cj = _media(chuvas_mm, DRIVERS); fonte = "drivers"
        if cj is None: raise ValueError("Nenhuma estação-driver encontrada.")
    acima = _media(chuvas_mm, ACIMA) or 0.0
    fa = [b.fracao_aberta_chuva for b in barragens if b.fracao_aberta_chuva is not None]
    fracao = sum(fa) / len(fa) if fa else None
    dv = sum(b.volume_retido_hm3 for b in barragens)
    vert = any(b.vertendo for b in barragens)
    nota = f"cj por {fonte}; ΔV do ato {dv:.1f} hm³ (" + ", ".join(f"{b.nome} {b.volume_retido_hm3:.1f}" for b in barragens) + ")"
    return estimar_pico(nivel_inicial, cj, acima, fracao, dv, vert, rede_completa, nota)


# ----------------------------------------------------------------------
# 4. PROJEÇÃO DE CRISTA PÓS-CHUVA (inalterada do v0.4; 2/2 validações)
# ----------------------------------------------------------------------
SEGUNDA_DIF_PADRAO = -0.075

def projetar_crista_pos_chuva(nivel_atual: float, taxa_atual_m_h: float,
                              segunda_dif: float = SEGUNDA_DIF_PADRAO) -> tuple[float, float]:
    nivel, taxa, t = nivel_atual, taxa_atual_m_h, 0.0
    while True:
        taxa += segunda_dif
        if taxa <= 0 or t >= 24:
            break
        nivel += taxa; t += 1.0
    return nivel, t


# ----------------------------------------------------------------------
# 5. VALIDAÇÃO EMBUTIDA (subconjunto; a tabela completa está no relatório)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # (nome, ni, cj, acima, fracao_aberta, dv_evento, vertendo, observado)
    CASOS = [
        ("14.1 (jun/26)", 1.85, 88.7, 0.0, 0.78, 13.9, False, 4.94),
        ("14.2 (jul/26)", 4.90, 57.7, 0.0, 0.00, 28.0, False, 6.36),
        ("15   (jul/26)", 2.77, 72.6, 66.4, 0.50, 20.3, False, 6.34),
        ("16   (jul/26)", 2.24, 96.8, 80.8, 0.58, 11.3, False, 5.94),
        ("Set26 (Ev17)", 3.26, 82.0, 73.7, 0.00, 62.9, False, 6.78),
        ("Jul23", 2.22, 118.2, 138.7, 0.05, 41.3, False, 7.35),
        ("I2 (mai/24)", 5.05, 48.0, 48.9, 0.63, 9.2, True, 7.47),
        ("J2 (jul/24)", 5.71, 58.0, 58.5, 0.22, 30.9, False, 7.43),
        ("B (out/23) vertendo", 6.54, 64.2, 56.6, 0.08, 82.1, True, 9.51),
        ("H (nov/23) chuva submedida", 5.85, 147.2, 57.2, 0.17, 163.8, True, 13.04),
        ("Set18", 1.28, 133.4, 120.0, 0.39, 48.2, False, 7.33),
        ("M22", 1.95, 189.7, 153.9, 0.49, 129.1, False, 9.74),
    ]
    print("=" * 78)
    print(f"ESTIMADOR v1.0 — s0={S0} b={B} k_acima={K_ACIMA} m_dv={M_DV} v_vert={V_VERT}")
    print("(erros EM AMOSTRA; os LOO estão em Analise_Estimador_v1_0.md)")
    print("=" * 78)
    for nome, ni, cj, ac, fa, dv, vt, obs in CASOS:
        e = estimar_pico(ni, cj, ac, fa, dv, vt)
        print(f"{nome:28s} pico {e.pico_central:5.2f} (obs {obs:5.2f}; erro {e.pico_central-obs:+.2f}) "
              f"banda {e.banda[0]:.2f}–{e.banda[1]:.2f} cj_ef {e.cj_efetiva_mm:5.0f}")
    print("\nSensibilidade s(h) m/100mm:", {h: round(sensibilidade(h), 2) for h in (1, 2, 4, 6, 8, 10)})
    print("\nExemplo API compatível (Set26 com BarragemV5):")
    bs = [BarragemV5("Sul", 0, 0, ocupacao_pct=43.7, ocupacao_inicio_pct=8.7, fracao_aberta_chuva=0.0),
          BarragemV5("Oeste", 0, 0, ocupacao_pct=28.4, ocupacao_inicio_pct=1.9, fracao_aberta_chuva=0.0)]
    print(estimar_pico_v5(3.26, {"Rio do Sul": 100.5, "Ituporanga": 62.8, "Taio": 120.6,
                                 "Aurora": 80.1, "Salete": 84.0, "Rio do Oeste": 64.6, "Laurentino": 68.8,
                                 "Pouso Redondo": 92.0, "Agrolandia": 76.2, "Trombudo Central": 85.1,
                                 "Agronomica": 67.2, "Alfredo Wagner": 42.1, "Rio do Campo": 91.6,
                                 "Taio_montante": 87.4}, bs))
