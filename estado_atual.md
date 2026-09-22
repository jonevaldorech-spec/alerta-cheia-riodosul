# Cheia — Rio do Sul (SC) — 2026-09-22 12:07 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 6.25 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 6.43 m · DC-RS Dom Tito: 6.25 m · offset medido DC-RS−SDC: -0.18 m
**Chuva 24h máx (drivers):** 89.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~6.25 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.019 m/h (anterior 0.0 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: sem dado · Trombudo Central: sem dado · Agrolandia: sem dado · ⚠ sem confirmação de régua-líder
- o v1.0 vira **TETO** (~6.7 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.7 m (banda p10–p90 6.2–7.2 m) → **Emergência**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 3.86 m em 21/09 18:03 (DC-RS) · subida até agora 2.39 m
- chuva-jusante do ato: 52.9 mm (ancoras; acumulado rolante ch24h do painel (histórico do ato insuficiente: 1 h, cobertura 6%)) · chuva-acima 50.4 mm
- cj efetiva 100 mm = cj 53 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 47 (ΔV do ato 66.8 hm³)
- sombra (cj_lat, c/ laterais): ~6.7 m (cj 50 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.6 m → Emergência (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 14.29 → 34.26 | 20.0 | 0.00 | 0A/7F | 15.04 m |  |
| Sul | 5.71 → 50.71 | 46.8 | 0.00 | 0A/5F | 25.05 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch24h do painel (histórico do ato insuficiente: 1 h, cobertura 6%)

| Município | Chuva do ato (mm) |
|---|---|
| Agrolandia | 82.6 |
| Ituporanga | 62.4 |
| Rio do Sul | 59.3 |
| Aurora | 53.5 |
| Salete | 49.8 |
| Trombudo Central | 47.2 |
| Rio do Oeste | 44.6 |
| Agronomica | 39.8 |
| Pouso Redondo | 38.2 |
| Taio | 37.2 |
| Laurentino | 33.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 57.2, Taio_montante 47.6, Alfredo Wagner 46.3

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 34.26 | 0A/7F | 0 | 15.04 m | 22/09 12:02 |
| Barragem Sul Ituporanga | 50.71 | 0A/5F | 0 | 25.05 m | 22/09 10:00 ❄ CONGELADO |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.18 m** · fallback -0.16 m
- **A) SDC-00013:** baseline 4.02 m · pico v1.0 ~6.9 m (banda 6.4–7.4) → **Emergência**
- **B) DC-RS Dom Tito:** baseline 3.86 m · pico v1.0 ~6.7 m (banda 6.2–7.2) → **Emergência**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 6.43 m · DC-RS 6.25 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 5.47 m

## ⚠ Avisos desta coleta

- Barragem Sul Ituporanga: sensor possivelmente CONGELADO na fonte (Asthon) — medida_em parada em 22/09 10:00 (~127 min; cadência normal ~30 min). % e montante podem estar desatualizados.
- Sensores TRAVADOS (descartados na fusão): 00022 ()
