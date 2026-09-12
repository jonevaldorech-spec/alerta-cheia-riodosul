# Cheia — Rio do Sul (SC) — 2026-09-12 08:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.71 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.89 m · DC-RS Dom Tito: 5.71 m · offset medido DC-RS−SDC: -0.18 m
**Chuva 24h máx (drivers):** 80.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.71 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.023 m/h (anterior -0.023 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~6.3 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.3 m (banda p10–p90 5.8–6.8 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 3.83 m em 11/09 06:42 (DC-RS) · subida até agora 1.88 m
- chuva-jusante do ato: 49.9 mm (ancoras; soma horária desde o vale (26 h, cobertura 100%)) · chuva-acima 60.9 mm
- cj efetiva 86 mm = cj 50 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 36 (ΔV do ato 50.5 hm³)
- sombra (cj_lat, c/ laterais): ~6.1 m (cj 41 mm · Δcj_lat−cj_v07 = -5.8 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.6 m → Emergência (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 14.87 → 45.74 | 30.9 | 0.00 | 0A/7F | 16.69 m |  |
| Sul | 0.58 → 19.4 | 19.6 | 0.00 | 0A/5F | 19.23 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (26 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Salete | 94.0 |
| Rio do Sul | 67.0 |
| Taio | 53.0 |
| Trombudo Central | 43.1 |
| Rio do Oeste | 42.4 |
| Laurentino | 41.4 |
| Pouso Redondo | 36.8 |
| Aurora | 36.6 |
| Agronomica | 36.2 |
| Agrolandia | 32.4 |
| Ituporanga | 29.5 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 92.2, Taio_montante 60.6, Alfredo Wagner 29.8

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 45.74 | 0A/7F | 0 | 16.69 m | 12/09 08:26 |
| Barragem Sul Ituporanga | 19.4 | 0A/5F | 0 | 19.23 m | 12/09 08:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.18 m** · fallback -0.15 m
- **A) SDC-00013:** baseline 3.98 m · pico v1.0 ~6.5 m (banda 6.0–7.0) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 3.83 m · pico v1.0 ~6.3 m (banda 5.8–6.8) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.89 m · DC-RS 5.71 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.7 m

## ⚠ Avisos desta coleta

- Kanitz possivelmente congelada (medida_em inalterada) — só checagem
- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
