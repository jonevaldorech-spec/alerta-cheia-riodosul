# Cheia — Rio do Sul (SC) — 2026-11-09 19:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 6.75 m — **EMERGÊNCIA** · tendência estável/caindo
- SDC-00013: 6.99 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 0.2 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~6.76 m → **EMERGÊNCIA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.044 m/h (anterior -0.01 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~7.1 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~7.1 m (banda p10–p90 6.4–7.8 m) → **Emergência**
**Classe que dispara o alerta/e-mail: EMERGÊNCIA**
- baseline = VALE do ato: 6.76 m em 09/11 19:15 (DC-RS) · subida até agora -0.01 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -59% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 0 (ΔV do ato 0.2 hm³) · **VERTENDO** (+0.37 m)
- sombra (cj_lat, c/ laterais): ~7.1 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~7.0 m → Emergência (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 78.24 → 78.41 | 0.2 | 0.00 | 0A/7F | 20.86 m |  |
| Sul | 108.75 → 108.75 | 0.0 | 0.00 | 0A/5F | 31.87 m | vertendo |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.1 |
| Trombudo Central | 0.1 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 0.1, Alfredo Wagner 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 78.41 | 0A/7F | 0 | 20.86 m | 09/11 19:26 |
| Barragem Sul Ituporanga | 108.75 | 0A/5F | 0.8699951171875 | 31.87 m | 09/11 19:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 7.0 m · pico v1.0 ~7.4 m (banda 6.6–8.0) → **Emergência**
- **B) DC-RS Dom Tito:** baseline 6.76 m · pico v1.0 ~7.1 m (banda 6.4–7.8) → **Emergência**
- **Δ pico (B − A): -0.30 m** · classe inalterada
- nível atual: SDC 6.99 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
