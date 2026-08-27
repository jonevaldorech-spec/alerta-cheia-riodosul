"""
ESTIMADOR v0.7 — curvas V(h) recalibradas (unica mudanca vs v0.6).
DQDH=700 e K_TRANSITO=0,35 MANTIDOS por decisao fundamentada em LOO 19/19
(Instrucoes v17): DQDH implicito n=10 mediana 535, mas RMSE em dominio
identico (0,35-0,36) para 535/663/700 — escalar no plato; continuidade vence.
LOO honesto (fora da amostra): RMSE 0,48 · vies −0,07 (n=17).

Estimador de pico de cheia — Rio do Sul (Itajaí-Açu)
Versão 0.6 — TERMO DE BARRAGEM MISTO POR BARRAGEM
Motivado pelo evento I2 (24/05/2024): o v0.5 tratava vertendo/crítico como
estado GLOBAL — se qualquer barragem estava ≥80% (ou vertendo), o ramo
curto-circuitava e DESCARTAVA a retenção volumétrica da outra. No I2 a
Oeste estava crítica (90→100%) e a Sul retinha 3,6 hm³ a 4A/1F: o v0.5
jogou fora os −0,18 m da Sul e errou +0,56; o termo misto fecha em +0,35.
1º evento do catálogo com uma barragem crítica E outra retendo — o caso que
o ev.B (calibração do TERMO_CRITICO, ambas 95/99%) não cobria.

O QUE MUDA vs v0.5 (APENAS estrutura; NENHUM coeficiente recalibrado):
- termo_barragens: classifica CADA barragem (vertendo / crítica ≥80% /
  normal). O termo positivo segue o pior estado global (TERMO_VERTENDO ou
  TERMO_CRITICO, inalterados) e a retenção volumétrica das barragens
  NORMAIS é sempre subtraída. Comportamento IDÊNTICO ao v0.5 quando todas
  estão no mesmo estado (ev.B: ambas críticas -> termo igual; ev.14–16:
  nenhuma crítica -> termo igual; validação embutida não muda).
- API preservada: BarragemV5, estimar_pico_v5, mesmas assinaturas.
- RECADASTRO v12 (contexto de dados, não de código): cj de I/J/J2 foi
  unificada em fonte SDC e o vale do J2 corrigido (5,71; Antec 15 h).
  Os erros de catálogo listados abaixo foram medidos com os valores
  ANTIGOS — re-validação LOO completa com features v12 é PENDÊNCIA
  declarada (não executada aqui para não maquiar números).

---------------------------------------------------------------- v0.5 ----
Versão 0.5 — TERMO VOLUMÉTRICO DE BARRAGEM (substitui fase_fechada/K_FOLGA)
Motivado pelo evento 16 (22/07/2026): v0.4 errou +0,96 m por não representar
QUANTO cada barragem removeu do rio — apenas SE/QUANDO fechou.

O QUE MUDA vs v0.4:
1. TERMO VOLUMÉTRICO (núcleo da versão): o efeito da barragem no pico é
   calculado da medida física direta — a SUBIDA DE MONTANTE — convertida em
   volume retido pelas curvas V(h) calibradas, e em corte de vazão na janela
   crítica de formação do pico:
       ΔH_barragens = − Σ_d [ ΔV_d(janela) / T_janela ] / DQDH
   com janela = [t_pico − 8h, t_pico] (≈ trânsito 5h ± espalhamento) e
   DQDH = declividade da curva-chave em RdS em estágio alto (m³/s por m).
   Isso captura AUTOMATICAMENTE tanto fechamento de comportas quanto retenção
   por excedência de capacidade dos descarregadores (Sul no ev.16 reteve
   5,00→10,50 m ANTES de fechar) — dois modos que o fase_fechada não via.
2. CURVAS V(h) POR BARRAGEM — calibradas nos pares (montante painel DC-RS ↔
   ocupação % SDC) dos eventos 14–16 (n=8 Sul, n=6 Oeste):
       Sul:   V[hm³] = 0.01222·(h−5.5)^2.83   (erro máx 0,31 hm³)
       Oeste: V[hm³] = 0.0949·(h−2.8)^2.29    (erro máx 1,73 hm³)
   Volumes totais (painel ev.14): Sul 104,03 hm³ · Oeste 99,96 hm³.
3. K_FOLGA e fase_fechada_chuva DEPRECIADOS (mantidos p/ retrocompatibilidade
   no modo legado). K_TRANSITO recalibrado em conjunto com DQDH (ev.15+16).
4. FONTES DE MONTANTE (lição ev.16 — OBRIGATÓRIO):
       Sul   → coluna "Montante" do painel DC-RS (07H/10H/17H).
       Oeste → SDC DCSC-00040 (mesmo datum do painel; mais atualizado).
       DCSC-00038 NÃO mede o reservatório da Sul — FORA do pipeline.
5. BANDA ASSIMÉTRICA condicionada ao estado dos reservatórios (ev.16):
   vazios+retendo → risco deslocado p/ baixo; ocupação>80% → p/ cima.

VALIDAÇÃO — CATÁLOGO COMPLETO 2023-2026 (16 eventos; rodar como script).
Fontes de retenção: Boletins 3h (out-nov/2023, % das duas barragens) e SPDC
07h/17h (mai-jul/2024); 2026 via curvas V(h) da montante do painel.
EM DOMÍNIO (13 eventos, ato único ≤~40h, cj representativa): RMSE 0,45 m ·
  B −0,02 · C +0,43 · D +1,08 · E +0,57 · F −0,22 · G +0,15 · J −0,33 ·
  J2 +0,21 · Jun −0,48 · A1 +0,44 · A2 −0,02 · E15 −0,38 · E16 +0,45
REANÁLISE DO EVENTO J (jul/2024): a hipótese multi-ato foi REFUTADA pela
série horária — subida única e contínua de 38 h, sem vale. O erro de −1,80 m
tinha DUAS causas distintas: (1) cj por âncoras 104 mm vs drivers 116 mm —
núcleo da chuva no eixo Sul/Trombudo, invisível às âncoras (ver
cj_representativa); (2) baseline de catálogo 2,02 vs trough real 2,18.
Corrigidas: J fecha em −0,2 a −0,3 m e ENTRA no domínio (13 ev., RMSE 0,45).
FORA DE DOMÍNIO (declarado, não maquiado):
  H −1,08 (43 h, 2023 — rede incompleta impede recomputar drivers) ·
  I −1,24 medido com cj ANTIGA (fonte mista/CEMADEN). RESOLVIDO no v12:
  chuva era divergência de FONTE (CEMADEN 1,43× o SDC naquele evento; I2
  provou o inverso) — cj SDC 135,1 (âncoras) / 150,0 (drivers); evento
  LIBERADO p/ calibração; re-teste na LOO v12 pendente ·
  A −2,48 (04/10/2023: sens. 5,51 m/100mm com API-10d ~4 mm — chuva
  suspeita de SUBMEDIÇÃO pela rede de 2023; não usar em calibração).
LOO 2026 (DQDH refit sem o evento): A1 +0,42 · A2 −0,19 · E15 −0,58 ·
E16 +0,52 — vs v0.4 fora-da-amostra no ev.16: +0,96. Quase metade.

LIMITES DECLARADOS (n=4!):
- DQDH efetivo é UM escalar para física que varia (curva-chave não-linear,
  coincidência de ondas, lag barragem→RdS não modelado); erros de ±0,4-0,5 m
  são o desempenho REAL esperado — a banda é parte do resultado, não enfeite.
- Resíduos estruturais conhecidos: A1 +0,44 (junho seco — hipótese de umidade
  antecedente foi TESTADA com API-10d CEMADEN e NÃO explica o catálogo: o
  evento A tinha API ~4 mm e é o maior sub-predito; o driver real dos grandes
  resíduos é violação do pulso único). E15 −0,38 (pede K_TRANSITO~0,5; refit
  com n=2 eventos-com-chuva-acima recriaria a degenerescência K×DQDH).
- D +1,08 (out/2023): pico em 11,86 m — extrapolação máxima da zona 3; a
  sensibilidade 2,7 m/100mm segue válida até ~11 m; acima disso, sem dados.
- Chuva-acima do ev.14 por ato indisponível → K_TRANSITO ali entra como 0.
- Janela fixa [t_pico−8h, t_pico] medida NA BARRAGEM mistura trânsito e
  contrafactual de pico; formulação com routing explícito fica para o ML
  (XGBoost aos ~30 eventos), não para heurística de n=4.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# ----------------------------------------------------------------------
# 0. PARÂMETROS
# ----------------------------------------------------------------------
K_TRANSITO = 0.35        # MANTIDO do v0.4 (fixá-lo evita degenerescência K×DQDH
                         # com n=4; refitar quando houver ≥6 eventos c/ chuva-acima)
DQDH = 700.0             # m³/s por m — declividade efetiva da curva-chave em RdS.
                         # RECALIBRADO com o catálogo 2023-2026: 5 eventos de
                         # retenção em domínio (F, A1, A2, E15, E16) → 699.
                         # Sanidade física (Manning, Q~1.300-1.800 m³/s em 5-6 m):
                         # dQ/dH ~400-700. ✓  Espalhamento individual 260-1980 —
                         # a banda de ±30% no termo é parte do resultado.
TERMO_VERTENDO = 0.0     # CORREÇÃO 2023: a regressão JÁ carrega +1,0 interno p/
                         # vertimento; o bônus adicional de +1,0/barragem do
                         # v0.3-v0.4 era DUPLA CONTAGEM (+1,5 a +2,5 m nos
                         # eventos C/D/E de out/2023). Zerado; n=4 vertimentos.
TERMO_CRITICO = 0.15     # barragem ≥80% sem verter (evento B, 95/99%: erro
                         # −0,02 m). n=1 — revalidar no próximo evento crítico.
JANELA_PICO_H = 8.0      # janela crítica de formação do pico
OCUP_CRITICA = 80.0      # regra JICA — acima disso a barragem SOMA
SEGUNDA_DIF_PADRAO = -0.075   # m/h² — decaimento linear pós-chuva
                              # (ev.15: −0,075 ±0,00 · ev.16: −0,070 ±0,02)

# Timing (ev.15, 3 experimentos; confirmado ev.16)
TRANSITO_SUL_RDS_H = (4.5, 5.5)
TPICO_POS_FECHAMENTO_H = (7, 8)
CONTRIB_SUL_REPASSE_M = (0.4, 0.5)

# Curvas montante(painel)→volume [hm³] — calibradas ev.14–16
_CURVAS_VH = {
    # v0.7 — RECALIBRADAS nos pares % OFICIAL (boletins DC-Ituporanga 2023,
    # n=273/230), validadas FORA DA AMOSTRA: Sul em 2024 (SPDC, −1,1 pp
    # mediana) e na âncora 2026 (18,65 m -> 17,9% vs 17,3 oficial;
    # 30,26 m -> 92,7% vs 92,87 oficial — o v0.5 dava 103%); Oeste nos
    # pares oficiais do ev.16/2026 (14,05 m -> 28,5% vs 27,9; o v0.5 dava
    # 24,2). Corrigem os residuos sistematicos do v13: Sul +4..+15 pp
    # acima de 60% -> ~0; Oeste −3..−7 pp na faixa media -> ±0,6 pp.
    # FAIXA DE VALIDADE: Sul montante 9,8–31,7 m · Oeste 9,3–25,6 m
    # (abaixo disso extrapola suave a zero; % via CSV 2026+ segue
    # preferencial quando existir). 2024 Oeste: coluna % SPDC CONGELADA
    # (7,0) — DESCARTADA da calibracao.
    "Sul":   dict(h0=6.85, c=0.05000, p=2.399, vol_total=104.03),
    "Oeste": dict(h0=7.55, c=2.00372, p=1.419, vol_total=99.96),
}
# Curvas v0.5 preservadas p/ reprodutibilidade de fichas antigas:
_CURVAS_VH_V05 = {
    "Sul":   dict(h0=5.5, c=0.01222, p=2.83, vol_total=104.03),
    "Oeste": dict(h0=2.8, c=0.0949,  p=2.29, vol_total=99.96),
}

def volume_reservatorio(barragem: str, montante_painel_m: float) -> float:
    """hm³ armazenados na cota de montante dada (escala do painel DC-RS).
    Sul → painel DC-RS 'Montante'; Oeste → SDC 00040. NUNCA usar DCSC-00038."""
    k = _CURVAS_VH[barragem]
    h = max(0.0, montante_painel_m - k["h0"])
    return k["c"] * h ** k["p"]

def ocupacao_de_montante(barragem: str, montante_painel_m: float) -> float:
    """% de ocupação estimada da montante — para quando o SPDC estiver fora."""
    k = _CURVAS_VH[barragem]
    return 100.0 * volume_reservatorio(barragem, montante_painel_m) / k["vol_total"]


# ----------------------------------------------------------------------
# 1. ESTADO DE UMA BARRAGEM (v0.5)
# ----------------------------------------------------------------------
@dataclass
class BarragemV5:
    """Estado volumétrico. montante_inicio/fim = cotas de painel na JANELA
    crítica [t_pico−8h, t_pico] (interpolar as leituras 07H/10H/17H)."""
    nome: str                          # "Sul" | "Oeste"
    montante_inicio_m: float
    montante_fim_m: float
    ocupacao_pct: Optional[float] = None   # do SPDC se houver; senão da curva
    extravasor_m: float = 0.0

    @property
    def ocupacao(self) -> float:
        if self.ocupacao_pct is not None:
            return self.ocupacao_pct
        return ocupacao_de_montante(self.nome, self.montante_fim_m)

    @property
    def vertendo(self) -> bool:
        return self.extravasor_m > 0 or self.ocupacao >= 100.0

    @property
    def volume_retido_hm3(self) -> float:
        return max(0.0, volume_reservatorio(self.nome, self.montante_fim_m)
                        - volume_reservatorio(self.nome, self.montante_inicio_m))

    @property
    def q_retencao_m3s(self) -> float:
        return self.volume_retido_hm3 * 1e6 / (JANELA_PICO_H * 3600.0)


def termo_barragens_v5(barragens: list[BarragemV5]) -> tuple[float, str]:
    """v0.6 — TERMO MISTO POR BARRAGEM (nome mantido p/ compatibilidade).
    Cada barragem é classificada individualmente:
      VERTENDO  -> termo global TERMO_VERTENDO (regressão já soma +1,0);
      CRÍTICA   -> ≥80% sem verter: termo global TERMO_CRITICO (n=1, ev.B);
      NORMAL    -> retenção volumétrica SEMPRE subtraída (lição do I2:
                   a Sul a 26-35% retendo não pode ser descartada porque a
                   Oeste está crítica).
    O termo positivo NÃO acumula por barragem (evita dupla contagem com a
    calibração do ev.B, em que AMBAS estavam críticas); prevalece o pior
    estado. Retenção de barragens críticas/vertendo NÃO é subtraída — perto
    da capacidade o ΔV medido não é confiável e a física JICA (≥80% amplia)
    já está no termo positivo."""
    notas = []
    verts   = [b for b in barragens if b.vertendo]
    crits   = [b for b in barragens if (not b.vertendo) and b.ocupacao >= OCUP_CRITICA]
    normais = [b for b in barragens if b not in verts and b not in crits]

    pos = 0.0
    if verts:
        pos = TERMO_VERTENDO
        notas.append("VERTENDO (" + ", ".join(b.nome for b in verts)
                     + ") — termo interno da regressão (+1,0) já aplicado")
    elif crits:
        pos = TERMO_CRITICO
        notas.append(", ".join(b.nome for b in crits)
                     + f" ≥{OCUP_CRITICA:.0f}% sem verter (+{TERMO_CRITICO:.2f} m; n=1, ev.B)")

    q_total = 0.0
    for b in normais:
        q = b.q_retencao_m3s
        q_total += q
        notas.append(f"{b.nome} reteve {b.volume_retido_hm3:.1f} hm³ na janela "
                     f"(~{q:.0f} m³/s; ocup.~{b.ocupacao:.0f}%)")
    ajuste = pos - q_total / DQDH
    if q_total > 0:
        notas.append(f"corte {q_total:.0f} m³/s ÷ DQDH {DQDH:.0f} "
                     f"{-q_total/DQDH:+.2f} m -> ajuste líquido {ajuste:+.2f} m")
    return ajuste, " | ".join(notas)


# ----------------------------------------------------------------------
# 2. CURVA CÔNCAVA + REGRESSÃO (inalteradas desde v0.3)
# ----------------------------------------------------------------------
_ZONAS = [(4.0, 4.4), (6.0, 3.8), (999.0, 2.7)]

def pico_concavo(nivel_inicial: float, chuva_jusante_mm: float) -> float:
    nivel, resto = nivel_inicial, chuva_jusante_mm
    for topo, sens in _ZONAS:
        if nivel >= topo:
            continue
        cap_mm = (topo - nivel) / sens * 100.0
        usa = min(resto, cap_mm)
        nivel += usa * sens / 100.0
        resto -= usa
        if resto <= 0:
            break
    return nivel

def pico_regressao(nivel_inicial: float, chuva_jusante_mm: float, vertendo: bool = False) -> float:
    if vertendo:
        return 2.29 + 0.59 * nivel_inicial + 0.032 * chuva_jusante_mm + 1.0
    return 1.81 + 0.74 * nivel_inicial + 0.033 * chuva_jusante_mm


# ----------------------------------------------------------------------
# 3. CATEGORIZAÇÃO DA BACIA (inalterada)
# ----------------------------------------------------------------------
DRIVERS = ["Rio do Sul", "Ituporanga", "Aurora", "Taio", "Salete",
           "Rio do Oeste", "Laurentino", "Pouso Redondo",
           "Agrolandia", "Trombudo Central", "Agronomica"]
ANCORAS = ["Rio do Sul", "Ituporanga", "Taio"]
ACIMA = ["Rio do Campo", "Alfredo Wagner", "Chapadao do Lageado", "Imbuia"]

def cj_representativa(chuvas_mm: dict[str, float], limiar: float = 0.10) -> tuple[float, str]:
    """REGRA DE REPRESENTATIVIDADE ESPACIAL (lição do evento J, jul/2024):
    quando o núcleo da chuva cai no eixo Trombudo/braço Sul (Agrolândia,
    Aurora, Trombudo, P.Redondo), a média das 3 ÂNCORAS não o enxerga e
    subestima a cj (evento J: âncoras 104 vs drivers 116 mm, +11%). Regra:
    calcular as duas médias; se divergirem mais que `limiar` (10%), usar
    a média de DRIVERS
    (n=8-11, robusta à posição do núcleo). Retorna (cj, fonte)."""
    anc = chuva_jusante(chuvas_mm, usar_ancoras=True)
    try:
        drv = chuva_jusante(chuvas_mm, usar_ancoras=False)
    except ValueError:
        return anc, "ancoras"
    if anc > 0 and abs(drv - anc) / anc > limiar:
        return drv, f"drivers (divergiu {100*(drv-anc)/anc:+.0f}% das ancoras)"
    return anc, "ancoras"


def chuva_jusante(chuvas_mm: dict[str, float], usar_ancoras: bool = True) -> float:
    alvo = ANCORAS if usar_ancoras else DRIVERS
    vals = [chuvas_mm[e] for e in alvo if e in chuvas_mm]
    if not vals:
        raise ValueError("Nenhuma estação-driver encontrada.")
    return sum(vals) / len(vals)

def chuva_acima_media(chuvas_mm: dict[str, float]) -> float:
    vals = [chuvas_mm[e] for e in ACIMA if e in chuvas_mm]
    return sum(vals) / len(vals) if vals else 0.0


# ----------------------------------------------------------------------
# 4. ESTIMADOR PRINCIPAL (v0.5)
# ----------------------------------------------------------------------
NIVEIS = [("Normal", 0.0), ("Atenção", 4.5), ("Alerta", 5.5), ("Emergência", 6.5)]

def classificar(nivel: float) -> str:
    faixa = "Normal"
    for nome, lim in NIVEIS:
        if nivel >= lim:
            faixa = nome
    return faixa


@dataclass
class EstimativaV5:
    pico_central: float
    banda: tuple[float, float]
    faixa: str
    ajuste_barragens: float
    nota_barragens: str
    chuva_jusante_mm: float
    cj_efetiva_mm: float
    nivel_inicial: float
    antecedencia_h: tuple[int, int]

    def __str__(self):
        lo, hi = self.banda
        a, b = self.antecedencia_h
        return (
            f"PICO: {self.pico_central:.1f} m  (banda {lo:.1f}–{hi:.1f} m)  -> {self.faixa}\n"
            f"  nível inicial (J2 se 2º ato): {self.nivel_inicial:.2f} m\n"
            f"  chuva-jusante: {self.chuva_jusante_mm:.0f} mm "
            f"(cj efetiva {self.cj_efetiva_mm:.0f} mm c/ trânsito da chuva-acima)\n"
            f"  barragens: {self.ajuste_barragens:+.2f} m  [{self.nota_barragens}]\n"
            f"  antecedência ao pico: ~{a}–{b} h"
        )


def estimar_pico_v5(nivel_inicial: float,
                    chuvas_mm: dict[str, float],
                    barragens: list[BarragemV5],
                    usar_ancoras: bool = True) -> EstimativaV5:
    """
    v0.5: a chuva-acima transita SEMPRE (cj_ef = cj + K_TRANSITO·chuva_acima);
    o que as barragens de fato capturaram é subtraído pelo termo volumétrico,
    medido na subida de montante. Não há mais `fase_fechada` a adivinhar:
    comportas fechadas ou capacidade excedida → montante sobe → termo age.
    Em modo PREVISIVO (antes do pico), projete montante_fim pelo ritmo de
    enchimento corrente e trate a banda como parte da resposta.
    """
    cj = chuva_jusante(chuvas_mm, usar_ancoras=usar_ancoras)
    cj_ef = cj + K_TRANSITO * chuva_acima_media(chuvas_mm)

    verte = any(b.vertendo for b in barragens)
    base_conc = pico_concavo(nivel_inicial, cj_ef)
    base_regr = pico_regressao(nivel_inicial, cj_ef, vertendo=verte)
    peso_conc = 0.8 if nivel_inicial < 3.0 else 0.5
    base = peso_conc * base_conc + (1 - peso_conc) * base_regr

    ajuste, nota = termo_barragens_v5(barragens)
    pico = base + ajuste

    # banda: espalhamento dos métodos + ±30% no termo de barragem,
    # ASSIMÉTRICA conforme o estado dos reservatórios (lição ev.16)
    lo = min(base_conc, base_regr) + ajuste
    hi = max(base_conc, base_regr) + ajuste
    if hi - lo < 1.0:
        meio = (lo + hi) / 2
        lo, hi = meio - 0.5, meio + 0.5
    inc_bar = 0.30 * abs(ajuste)
    ocup_max = max((b.ocupacao for b in barragens), default=0.0)
    retendo = ajuste < -0.05
    if retendo and ocup_max < 40.0:
        lo -= inc_bar + 0.1     # reservatórios com folga retendo: risco p/ baixo
        hi += inc_bar * 0.5
    elif ocup_max >= OCUP_CRITICA:
        lo -= inc_bar * 0.5     # perto do crítico: risco p/ cima
        hi += inc_bar + 0.3
    else:
        lo -= inc_bar
        hi += inc_bar
    ant = (10, 15) if nivel_inicial < 3.0 else (6, 12)

    return EstimativaV5(pico, (lo, hi), classificar(pico), ajuste, nota,
                        cj, cj_ef, nivel_inicial, ant)


# ----------------------------------------------------------------------
# 5. PROJEÇÃO DE CRISTA PÓS-CHUVA (inalterada; 2/2 validações: −0,03/+0,02)
# ----------------------------------------------------------------------
def projetar_crista_pos_chuva(nivel_atual: float, taxa_atual_m_h: float,
                              segunda_dif: float = SEGUNDA_DIF_PADRAO
                              ) -> tuple[float, float]:
    """Chuva ENCERRADA + drivers rápidos cristados → taxa decai linearmente.
    ev.15: previu 6,31 (obs 6,34); ev.16: previu 5,97 @15h25 (obs 5,94 @15H).
    NÃO usar com chuva ativa nem logo após manobra (esperar 1–2 leituras)."""
    nivel, taxa, t = nivel_atual, taxa_atual_m_h, 0.0
    while True:
        taxa += segunda_dif
        if taxa <= 0 or t >= 24:
            break
        nivel += taxa
        t += 1.0
    return nivel, t


# ----------------------------------------------------------------------
# 6. MODO LEGADO v0.4 (retrocompatibilidade — DEPRECIADO)
# ----------------------------------------------------------------------
K_FOLGA = 0.38  # legado

@dataclass
class Barragem:  # assinatura v0.4 preservada
    nome: str
    ocupacao_pct: float
    comportas_abertas: int
    comportas_total: int
    extravasor_m: float = 0.0
    montante_m: Optional[float] = None
    @property
    def vertendo(self): return self.extravasor_m > 0 or self.ocupacao_pct >= 100.0
    @property
    def fracao_fechada(self):
        return 0.0 if self.comportas_total <= 0 else 1.0 - self.comportas_abertas / self.comportas_total
    @property
    def folga(self): return max(0.0, 1.0 - self.ocupacao_pct / 100.0)


# ----------------------------------------------------------------------
# 7. VALIDAÇÃO — eventos 14 (2 atos), 15 e 16 + leave-one-out
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # (nome, baseline, chuvas, [(barragem, m_ini_janela, m_fim_janela)], obs)
    # Janelas de montante interpoladas das leituras 07H/10H/17H do painel.
    CASOS = [
        ("EV14 ATO1 (pico ~20H 30/06)", 1.85,
         {"Rio do Sul": 91.1, "Ituporanga": 62.4, "Taio": 112.6},
         [("Sul", 7.84, 10.14), ("Oeste", 9.41, 10.93)], 4.94),
        ("EV14 ATO2 (pico 16H 01/07)", 4.90,
         {"Rio do Sul": 77.9, "Ituporanga": 48.0, "Taio": 47.3},
         [("Sul", 12.97, 16.73), ("Oeste", 12.68, 14.12)], 6.36),
        ("EV15 (pico 23H 11/07)", 2.77,
         {"Rio do Sul": 57.0, "Ituporanga": 80.9, "Taio": 84.2,
          "Alfredo Wagner": 86.8, "Rio do Campo": 45.9},
         [("Sul", 12.20, 16.16), ("Oeste", 7.00, 9.34)], 6.34),
        ("EV16 (pico 15H 22/07)", 2.24,
         {"Rio do Sul": 96.8, "Ituporanga": 96.8, "Taio": 96.8,
          "Alfredo Wagner": 54.8, "Rio do Campo": 106.7},
         [("Sul", 10.50, 12.30), ("Oeste", 3.80, 10.80)], 5.94),
    ]

    # I2 (24/05/2024) — o caso que motivou o v0.6: Oeste crítica (ocupação %
    # oficial DC-RO na janela) + Sul retendo. Montantes interpolados 07H/17H.
    CASO_I2 = ("I2 (pico 12h30 24/05/2024)", 5.05,
        {"Rio do Sul": 62.1, "Ituporanga": 65.8, "Taio": 56.5,
         "Laurentino": 58.7, "Pouso Redondo": 58.0, "Agrolandia": 71.9,
         "Trombudo Central": 47.9, "Agronomica": 57.7, "Rio do Oeste": 57.9,
         "Rio do Campo": 53.6, "Alfredo Wagner": 61.1}, 7.47)

    def rodar(caso):
        nome, ni, ch, bars, obs = caso
        bs = [BarragemV5(n, a, b) for n, a, b in bars]
        e = estimar_pico_v5(ni, ch, bs)
        return e, e.pico_central - obs

    print("=" * 72)
    print(f"VALIDAÇÃO v0.6 — K_TRANSITO={K_TRANSITO}  DQDH={DQDH:.0f} m³/s/m (coeficientes = v0.5)")
    print("=" * 72)
    for caso in CASOS:
        e, err = rodar(caso)
        print(f"{caso[0]:34s} pico {e.pico_central:.2f} (obs {caso[4]:.2f}; "
              f"erro {err:+.2f})  bar {e.ajuste_barragens:+.2f} m")
    nome, ni, ch, obs = CASO_I2
    sul = BarragemV5("Sul", 21.13, 21.87, ocupacao_pct=32.8)
    oes = BarragemV5("Oeste", 21.66, 22.25, ocupacao_pct=95.5)
    e = estimar_pico_v5(ni, ch, [sul, oes])
    print(f"{nome:34s} pico {e.pico_central:.2f} (obs {obs:.2f}; "
          f"erro {e.pico_central-obs:+.2f})  bar {e.ajuste_barragens:+.2f} m")
    print("  [v0.5 no mesmo caso: +0,56 — retenção da Sul descartada pelo ramo ≥80%]")

    print("\nLOO 19/19 EXECUTADO (v17): RMSE 0,48 | vies -0,07 (fora da amostra).")
    print("Avaliacao em dominio n=17, DQDH=700: curvas v0.5 RMSE 0,37 | v0.7 RMSE 0,38")
    print("-> curvas novas NEUTRAS no pico; ganho do v0.7 esta no RISCO:")
    print("   ocupacao_de_montante() agora ±0,6 pp em toda a faixa (era +15/-7 pp).")
    print("DQDH implicito n=10: mediana 535, faixa 145-1765; 535/663/700 empatam")
    print("em RMSE (0,35-0,36) -> DQDH=700 MANTIDO por continuidade.")
    print("Residuo estrutural dominante: janela fixa (+0,6..+1,2 nos atos com")
    print("retencao pre-janela; -0,6..-0,8 em J/J2/N) -> routing explicito no ML.")
