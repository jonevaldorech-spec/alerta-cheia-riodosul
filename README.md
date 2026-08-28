# Alerta de Cheia — Rio do Sul (bacia do Alto Itajaí)

Coleta automática, **na nuvem do GitHub (com o seu PC desligado)**, dos dados
das estações da bacia que alimentam o modelo de previsão de cheia da **cidade de
Rio do Sul (SC)**.

A cada 30 minutos, o GitHub roda o `coletor.py`, que puxa **duas fontes públicas
oficiais**, **funde as estações por município**, roda o **estimador v0.9**, guarda
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
- `estimador.py` — estimador de pico v0.9 (cópia do `estimador_pico_v0_9.py`).
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

O pico estimado no e-mail usa o **estimador v0.9** do projeto
(`estimador.py`: curvas côncava + regressão + trânsito da chuva-acima + termo de
barragem), alimentado automaticamente com:
- **baseline** = mínimo do nível de Rio do Sul nas últimas 48 h (disciplina do
  projeto: nunca usar o nível em subida como inicial);
- **chuva-jusante** = acumulada 48 h **fundida por município** (`fusao_estacoes`),
  chamada com `usar_ancoras=False` (a lista DRIVERS já cobre âncoras + drivers);
- **barragens** = estado (% de ocupação / vertimento) da Asthon, em **modo
  conservador**: classifica o estado mas **não credita o peak-shaving
  volumétrico** (que exige a janela de montante do painel, interpolada à mão).
  Para um alerta, não-creditar é o lado seguro — o pico automático fica
  ~0,5–1 m **acima** do estimador rodado à mão nos eventos com barragem segurando.

O e-mail traz o pico **OFICIAL** (`cj_v07`, sem laterais) e, em paralelo, o
**pico-sombra** (`cj_lat`, com laterais) + o Δ — protocolo de calibração
prospectiva. Para o número fino durante um evento, cole os dados no chat do
projeto e rode o `estimador.py` com as janelas de montante. Se `estimador.py`/
`fusao_estacoes.py` não puderem ser importados, o coletor grava só os dados crus.

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
