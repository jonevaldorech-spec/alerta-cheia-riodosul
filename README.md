# Alerta de Cheia — Rio do Sul (bacia do Alto Itajaí)

Coleta automática, **na nuvem do GitHub (com o seu PC desligado)**, dos dados
das estações da bacia que alimentam o modelo de previsão de cheia da **cidade de
Rio do Sul (SC)**.

A cada 30 minutos, o GitHub roda o `coletor.py`, que puxa **duas fontes públicas
oficiais**, **funde as estações por município**, roda o **estimador v1.0**, guarda
a série no próprio repositório (histórico automático dos eventos) e, **quando
detecta um evento**, te manda um **e-mail de alerta** com o nível de Rio do Sul,
o pico estimado e o estado das barragens.

## Fusão de estações (fusao_estacoes v0.3)
Antes do estimador, as réguas são fundidas por município (média das pares — ex.:
Ituporanga = 00085+00039, Taió-jusante = 00041+00171), com **descarte de sensor
travado** (leitura > 60 min atrasada) e de **0,0 anômalo** na chuva. O pico
**OFICIAL** usa `cj_v07` (sem laterais — continuidade com a curva calibrada); um
**pico-sombra** `cj_lat` (com as laterais Petrolândia/Atalanta/Mirim Doce/Braço
do Trombudo) é calculado em paralelo e o Δ é logado, conforme o protocolo de
calibração prospectiva do projeto.

## Fontes coletadas
1. **Estado (Defesa Civil SC)** — `monitoramento.defesacivil.sc.gov.br/graphql`
   (plataforma "Qualle"). Níveis + chuva de todas as estações da bacia, inclusive
   **Ituporanga (00039)** e **Taió (00041)**, que a Asthon não tem.
2. **Rio do Sul (Asthon)** — `public.asthon.com.br` — barragens Sul e Oeste
   **comporta a comporta** (% de ocupação, comportas A/F, montante).

## O que fica no repositório
- `coletor.py` — coletor + fusão + estimador (roda a cada 30 min).
- `estimador.py` — estimador de pico **v1.0** (cópia do `estimador_pico_v1_0.py`; ver `Analise_Estimador_v1_0.md`).
- `estimador_v09.py` — modelo antigo (v0.9), roda só para comparação no `estado_atual.md`.
- `fusao_estacoes.py` — fusão por município (cópia do `fusao_estacoes_v0_3.py`).
- `dados/serie_bacia.csv` — 1 linha por **estação crua** por coleta (auditoria; a série cresce sozinha).
- `dados/barragens.csv` — 1 linha por barragem por coleta.
- `estado_atual.md` — a situação atual, legível aqui no GitHub (abre e vê as tabelas).
- `evento.txt` — `SIM`/`NAO` (usado internamente para decidir o e-mail).

---

## Instalação (uma vez só, ~5 min)

### 1. Criar o repositório
1. Crie uma conta grátis em https://github.com (se já tiver, pule).
2. Clique em **New repository**. Nome: `alerta-cheia-riodosul`.
   - Deixe **Public** (recomendado: repositório público = minutos de Actions
     **ilimitados**; os dados são públicos mesmo, então não há problema).
3. **Add file → Upload files** e arraste TODO o conteúdo desta pasta
   (`coletor.py`, a pasta `.github`, a pasta `dados`, este `README.md`).
   Confirme em **Commit changes**.

### 2. Ligar o Actions
- Vá na aba **Actions** do repositório e clique em **"I understand my workflows,
  go ahead and enable them"**.
- Para testar na hora: Actions → *Coleta e alerta de cheia* → **Run workflow**.
  Em ~1 min aparece um commit novo e o `estado_atual.md` atualizado.

Pronto — a partir daí ele roda **sozinho a cada 30 min**, PC ligado ou não.

---

## Receber o alerta por e-mail

Há dois modos. Escolha UM.

### Modo simples (sem configurar nada): Issue
Se você **não** configurar o e-mail abaixo, quando houver evento o robô abre uma
**Issue** no repositório. O GitHub te manda um e-mail dessa issue automaticamente
(confira em https://github.com/settings/notifications que "Issues" está ligado).

### Modo e-mail direto (Gmail) — recomendado
Manda um e-mail de verdade para `jonevaldo.rech@gmail.com`.
1. Ative a verificação em 2 etapas na Conta Google (necessário para o próximo passo).
2. Crie uma **Senha de app**: https://myaccount.google.com/apppasswords →
   nome "GitHub Alerta Cheia" → copie os 16 caracteres.
3. No repositório: **Settings → Secrets and variables → Actions → New repository
   secret** e crie:
   - `MAIL_USERNAME` = seu Gmail (ex.: `jonevaldo.rech@gmail.com`)
   - `MAIL_PASSWORD` = a senha de app de 16 caracteres (sem espaços)
   - `MAIL_TO` = para onde mandar (opcional; padrão = seu próprio Gmail)

Com os secrets cadastrados, o modo Gmail assume automaticamente e o modo Issue
fica desligado.

> Durante um evento longo você recebe um e-mail a cada 30 min (é de propósito —
> é uma cheia em andamento). Para afrouxar, mude o `cron` em
> `.github/workflows/coleta.yml`.

---

## Quando é considerado "evento"
- Rio do Sul em **Atenção** (≥ 4,5 m), **Alerta** (≥ 5,5) ou **Emergência** (≥ 6,5); **ou**
- Rio do Sul subindo **e** chuva 24h ≥ 30 mm em algum driver; **ou**
- chuva 24h ≥ 50 mm em algum driver.

O pico estimado no e-mail usa o **estimador v1.0** do projeto (`estimador.py`:
curva côncava suave + trânsito da chuva-acima por fração de comportas abertas +
enchimento das barragens no ato como chuva implícita + vertimento; calibrado e
validado em 43 atos de 2018–2026 — LOO 0,39 m nos atos calibráveis, 0,71 m no
total). Ele é alimentado com as grandezas **do ato**, não com acumulados rolantes:
- **baseline** = **vale do ato** detectado na régua de referência (últimas 96 h):
  o mínimo antes de o rio voltar a ficar >0,25 m acima dele (= recessão do ato
  anterior). Num 2º/3º ato é o trough entre atos (convenção J2); sem série, cai no
  "mín 48 h" antigo e avisa;
- **chuva-jusante** = **soma horária desde o vale**, por estação, a partir do
  próprio histórico do coletor (`dados/serie_bacia.csv`, `chuva_1h`, um snapshot
  por hora), **fundida por município** (`fusao_estacoes`) e com a regra
  âncoras→drivers (>10 % de divergência). Se o histórico do ato tiver cobertura
  < 70 %, usa o acumulado do painel cuja janela cobre as horas desde o vale
  (6/24/48/72 h) e diz isso no md;
- **barragens** = **ΔV retido desde o vale** (% da Asthon no vale → agora, ×
  volume total) e **fração média de comportas abertas** desde o vale
  (`dados/barragens.csv`), mais o flag de vertimento. Não existe mais "crédito
  fino/conservador": o termo de barragem é observado, não estimado.

O e-mail traz o pico **OFICIAL** (`cj_v07`, sem laterais; banda p10–p90 dos
resíduos reais) e, em paralelo, o **pico-sombra** (`cj_lat`, com laterais) + o Δ,
além do **pico do modelo antigo v0.9** (só comparação). A classe do alerta é a do
pico central do v1.0 (ou a faixa atual do rio, o que for maior). Se `estimador.py`/
`fusao_estacoes.py` não puderem ser importados, o coletor grava só os dados crus.

Na **fase final do evento** entra o **MODO CRISTA** (nowcast): quando a
chuva-driver encerrou, as réguas-líder (Pouso Redondo/Trombudo/Agrolândia) já
cristaram e o rio ainda sobe mas desacelera, o número principal passa a ser a
**projeção da trajetória** (`projetar_crista_pos_chuva`, validado a ~3 cm nos
ev.15/16) e o v1.0 vira **teto**. Perto da crista, um modelo "chuva entra, pico
sai" perde para a trajetória já observada; é aí que se chega à precisão de ~10 cm
que a previsão antecipada não alcança. A classe do alerta segue a projeção, nunca
abaixo da faixa atual do rio.

> O histórico do ato vem do próprio repositório: nas primeiras horas depois de
> ligar o robô (ou após uma lacuna de coleta) a soma desde o vale pode ficar
> incompleta — o md informa a cobertura e o método usado.

## Ajustes rápidos
- **Cadência:** linha `cron` no workflow. `*/15 * * * *` = 15 min (repo público).
- **Estações monitoradas:** dicionário `ALVO` no `coletor.py`.
- **Limiar de evento:** função/variáveis no fim do `main()` do `coletor.py`.

## Observações
- O GitHub **pausa** workflows agendados após 60 dias sem commits no repo. Como o
  robô commita a cada coleta, isso não acontece enquanto estiver rodando; se um
  dia pausar, é só fazer qualquer commit para religar.
- O histórico das fontes começou em ~28/07/2026 (Asthon). Para dados anteriores,
  valem as fontes de sempre do projeto.
