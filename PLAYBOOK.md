---
name: cheia-rio-do-sul
description: >-
  Assistente operacional do sistema de previsão e alerta de cheia da CIDADE DE
  RIO DO SUL (Alto Vale do Itajaí, SC). Use SEMPRE que o usuário mencionar
  cheia, enchente, nível do rio, cota, subida do rio, barragem (Sul/Ituporanga
  ou Oeste/Taió), comportas, vertimento ou repasse em Rio do Sul ou no Alto
  Vale; quiser o PICO ESTIMADO de uma cheia; precisar interpretar dados das
  estações da Defesa Civil de SC (monitoramento.defesacivil.sc.gov.br ou a
  plataforma Asthon); acompanhar um evento em andamento em tempo real; rodar o
  estimador de pico; ou pedir ajuda com "meu projeto de cheia", o repositório
  alerta-cheia-riodosul, o coletor, a fusão de estações ou o estimador. Traz o
  playbook operacional, as APIs das duas fontes já decifradas, os limiares e
  lags da bacia, e o código do estimador e da fusão de estações.
---

# Cheia — Rio do Sul (Alto Vale do Itajaí, SC)

Sistema de **previsão e alerta de cheia da cidade de Rio do Sul**. O objetivo é
estimar (a) o **nível de pico** e (b) a **antecedência** (horas até a água
subir), a partir dos dados das estações a montante e do estado das barragens,
para dar **alerta antecipado** à população/comércio.

Esta skill é o **modo operacional**: use-a para acompanhar um evento, puxar os
dados ao vivo, rodar o estimador e interpretar a situação. O histórico completo
de pesquisa está em `references/instrucoes_projeto_v25.md` (consulte para dúvidas
hidrológicas profundas) e a topologia em `references/topologia_bacia_v14.md`.

## O sistema automático já no ar
Um coletor roda **a cada 30 min na nuvem do GitHub** (disparado pelo cron-job.org,
PC desligado), puxa as duas fontes, funde as estações, roda o estimador e **manda
e-mail se houver evento**. Repositório **público**:
`https://github.com/jonevaldorech-spec/alerta-cheia-riodosul`

**Para ver a situação atual de qualquer PC**, busque (WebFetch) o snapshot cru:
```
https://raw.githubusercontent.com/jonevaldorech-spec/alerta-cheia-riodosul/main/estado_atual.md
```
Séries acumuladas: `dados/serie_bacia.csv` (estações cruas) e `dados/barragens.csv`
no mesmo repo (troque o caminho na URL raw).

---

# PLAYBOOK — acompanhar um evento ao vivo

Faça nesta ordem:

### 1. Puxar o estado atual
Preferência: rodar `scripts/coletor.py` (puxa as 2 fontes, funde, estima) num
diretório com internet — gera `estado_atual.md`, `dados/serie_bacia.csv`,
`dados/barragens.csv`. Se não puder rodar Python, faça WebFetch do `estado_atual.md`
raw (link acima) ou consulte as APIs direto (seção "Fontes de dados").

### 2. Fixar o BASELINE (erro clássico — não repita)
O nível inicial do estimador é o **baseline PRÉ-evento**, NUNCA o nível em subida.
Use o **mínimo do nível de Rio do Sul (DCSC-00013) nas últimas 48 h** (o coletor já
faz isso via a query `Historic`). Num 2º ato, o inicial é o **trough entre atos**.
> Uma vez, usar o nível de subida como inicial inflou uma projeção em ~1,33 m.

### 3. Estimar o pico
Rode o estimador (seção "Estimador"). O número que **DECIDE** é o `cj_v07` (sem
laterais). O `cj_lat` (com laterais) roda em **sombra** e o Δ é anotado.

### 4. Interpretar e decidir (GO/NO-GO)
- **Faixas de Rio do Sul (m):** Normal <4,5 · **Atenção ≥4,5** · **Alerta ≥5,5** ·
  **Emergência ≥6,5**.
- Disparar preparação quando **Pouso Redondo/Agrolândia/Trombudo subindo forte**
  (dá ~8–12 h) **e/ou** chuva a jusante das barragens acumulando.
- **Rio recuou mas a cabeceira voltou a chover → NÃO desarmar** (risco de 2º ato).
- No **2º ato com solo saturado**, a janela de aviso pelas estações de montante
  encolhe para **~4–6 h** — nesse regime decida pela **chuva** (prevista + caindo),
  não pelo nível de montante.
- Nível já alto (>5 m): pouca chuva basta para inundar.
- Vigie **ocupação % e extravasor** (não a montante em metros) para risco de
  vertimento; e o momento em que as barragens **reabrem comportas** (repasse).
- **Manobra de comporta** (painéis não avisam a tempo): salto/queda **>0,3 m/h no
  00039 (Sul) ou 00171 (Oeste) sem chuva** = manobra. Fechamento na subida →
  projete `t_pico ≈ fechamento + 7–8 h`.
- **Chuva encerrada** → projete a crista pelo **decaimento LINEAR** da taxa
  (`projetar_crista_pos_chuva`), não pelo geométrico.

---

# Fontes de dados (APIs decifradas — ambas públicas, sem login)

### 1. Estado — Defesa Civil de SC ("Qualle", GraphQL, **POST-apenas**)
- Endpoint: `https://monitoramento.defesacivil.sc.gov.br/graphql`
- **Segredo:** parâmetro `client = "secretaria-de-defesa-civil"`.
- `Tags_data` → todas as ~174 estações, valores atuais (nível + chuva
  1h/6h/24h/48h/72h + timestamp UTC).
- `Historic(stationCode, startDate, endDate, interval)` → série por estação,
  intervalos `MIN_5`..`HOUR_168`. `system: Qualle_Hidrometeorologia`.
- Códigos = os DCSC do projeto (Rio do Sul 00013, Ituporanga 00039, Taió 00041…).
- Introspecção habilitada; o timestamp do `Tags_data` é UTC, o do `Historic` já é
  local. O código exato das duas queries está em `scripts/coletor.py`.

### 2. Rio do Sul — plataforma Asthon (REST/JSON)
- Base `https://public.asthon.com.br/public`, `city_id=4214805`.
- `dams?city_id=4214805` → **barragens Sul e Oeste comporta a comporta**
  (% ocupação, comportas A/F, montante, vertido). É a MELHOR fonte das barragens.
- `stations/live`, `stations/list`, `station-history` também disponíveis.
- **Bloqueia o User-Agent padrão do Python** → mande um UA próprio.
- Histórico começa ~28/07/2026 (não serve para eventos anteriores).

> ⚠ A nuvem de agente do Claude (rotinas) tem firewall que BLOQUEIA esses dois
> domínios, e o site estadual é POST (WebFetch não alcança). Por isso a coleta
> roda no GitHub Actions, não numa rotina Claude. De um Claude Code com internet
> aberta (PC local), `scripts/coletor.py` funciona direto.

---

# Estimador de pico (estimador v0.9 + fusão v0.3)

`scripts/estimador.py` e `scripts/fusao_estacoes.py`. API pública estável:
`estimar_pico_v5(nivel_inicial, chuvas_mm, barragens, usar_ancoras=False)`.

### Entradas
- **nivel_inicial**: baseline (mín 48 h de Rio do Sul).
- **chuvas_mm**: dict `{município: mm}` da **chuva-jusante fundida** (acumulada 48 h
  como proxy do evento). Monte com `fusao_estacoes.dicts_para_estimador(leituras)`,
  que devolve `(chuvas_v07, chuvas_lat)` já com a chuva-acima. **Chame o estimador
  com `usar_ancoras=False`** — a lista DRIVERS da v0.9 já inclui âncoras + drivers +
  laterais, então `chuvas_v07` dá o cj OFICIAL e `chuvas_lat` o cj SOMBRA.
- **barragens**: `[BarragemV5("Sul", montante_ini, montante_fim, ocupacao_pct=…),
  BarragemV5("Oeste", …)]`.

### O número FINO das barragens (peak-shaving) — passo manual
O termo de barragem depende da **subida de montante na janela [t_pico−8h, t_pico]**,
na **escala do PAINEL** (não a da estação SDC da barragem!):
- **Sul** → coluna "Montante" do painel DC-RS (ou a `nivel_m` da Asthon convertida).
- **Oeste** → SDC **DCSC-00040** (mesmo datum do painel). **NUNCA** use a 00038 p/ Sul.
Interpole as leituras 07h/10h/17h para a janela. A curva V(h) converte em volume
retido → corte de vazão → −ΔH. **O coletor automático NÃO faz isso** (roda em modo
conservador, sem crédito de shaving → fica ~0,5–1 m acima); para o número fino,
forneça `montante_ini`/`montante_fim` reais.

### Modo previsivo (antes do pico)
Projete `montante_fim` pelo ritmo de enchimento corrente e trate a **banda** como
parte do resultado (o erro real esperado é ±0,4–0,5 m — a banda não é enfeite).

Rode o próprio `scripts/estimador.py` como script (`python estimador.py`) para ver a
validação nos eventos 14/15/16/I2.

---

# Referência rápida da bacia

### Duas vias de aviso
- **Braço Sul** (Itajaí do Sul): rápido, avisa pouco (~3–4 h). Barragem Sul em
  Ituporanga. Trânsito barragem→RdS **4,5–5,5 h** (constante validada 3+ vezes).
- **Tronco Oeste** (Itajaí do Oeste) + **Trombudo**: onda lenta e larga (~8–12 h).
  Barragem Oeste em Taió (enche e verte ANTES — ~4× menos vertedouro).

### Lags típicos até Rio do Sul (encurtam com bacia cheia)
Pouso Redondo ~9–10 h · Agrolândia ~8–9 h · Trombudo Central ~8 h · Ituporanga
~3–5 h (barragem distorce) · Rio do Oeste/Laurentino/Agronômica ~0 h (confirmam,
não avisam). **Solo saturado encurta tudo em 2–3 h.**

### Físicas estabelecidas
- Pico governado pela **chuva ABAIXO das barragens** (r≈0,90), não a total (r≈0,46).
- Curva cota-volume **côncava**: sensibilidade cai de ~4,4 (inicial <4 m) → ~3,8
  (4–6 m) → ~2,7 (>6 m). Partindo alto, a mesma chuva sobe MENOS — mas inunda com
  pouca chuva.
- Barragens: **% de ocupação** (não a montante em metros) decide o regime.
  ≥80–100% ou extravasor>0 → **VERTE** (soma à cheia); com folga e comportas
  fechadas → **peak-shaving** (subtrai).

### Regras da fusão de estações (fusao_estacoes v0.3)
- Fusão = **média** das réguas do município (pares travados em 28/08/2026).
- **Descarta sensor TRAVADO** (última leitura > 60 min atrasada) — chuva e nível.
- **Descarta 0,0 anômalo** só na chuva, só quando a irmã tem volume significativo.
- Taió separa lados: cj usa só o par **jusante** (00041+00171); **00066** (montante)
  vai para chuva-acima (`Taio_montante`).
- Laterais (Petrolândia 00146 / Atalanta 00086 / Mirim Doce 00162 / Braço do
  Trombudo 00129) entram só no cj **sombra** (`incluir_laterais=True`), até a
  recalibração pré-registrada fechar (≥6 atos pareados).

---

# Estrutura dos arquivos desta skill
- `scripts/estimador.py` — estimador de pico v0.9 (curvas V(h) + termo de barragem).
- `scripts/fusao_estacoes.py` — fusão por município v0.3 (cj_duplo, dicts_para_estimador).
- `scripts/coletor.py` — coletor das 2 fontes + fusão + estimador (o que roda no GitHub).
- `references/instrucoes_projeto_v25.md` — log completo de pesquisa (fonte da verdade
  para hidrologia; consulte para catálogo de eventos, calibrações, decisões).
- `references/topologia_bacia_v14.md` — topologia detalhada da bacia (estações, cadeias).

Ao ajudar num evento, prefira citar dado VERIFICADO e marcar claramente o que é
ESTIMATIVA. O erro real do estimador é ±0,4–0,5 m — a banda faz parte da resposta.
