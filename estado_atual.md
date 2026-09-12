# Cheia — Rio do Sul (SC) — 2026-09-12 11:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.64 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.81 m · DC-RS Dom Tito: 5.64 m · offset medido DC-RS−SDC: -0.17 m
**Chuva 24h máx (drivers):** 64.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.65 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.025 m/h (anterior -0.026 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~6.4 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.4 m (banda p10–p90 5.9–6.9 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 3.83 m em 11/09 06:42 (DC-RS) · subida até agora 1.81 m
- chuva-jusante do ato: 49.9 mm (ancoras; soma horária desde o vale (29 h, cobertura 100%)) · chuva-acima 60.9 mm
- cj efetiva 89 mm = cj 50 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 39 (ΔV do ato 54.5 hm³)
- sombra (cj_lat, c/ laterais): ~6.2 m (cj 41 mm · Δcj_lat−cj_v07 = -5.8 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.6 m → Emergência (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 14.87 → 48.85 | 34.0 | 0.00 | 0A/7F | 17.12 m |  |
| Sul | 0.58 → 20.3 | 20.5 | 0.00 | 0A/5F | 19.45 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (29 h, cobertura 100%)

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
| Barragem Oeste Taió | 48.85 | 0A/7F | 0 | 17.12 m | 12/09 10:56 |
| Barragem Sul Ituporanga | 20.3 | 0A/5F | 0 | 19.45 m | 12/09 10:56 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.17 m** · fallback -0.155 m
- **A) SDC-00013:** baseline 3.98 m · pico v1.0 ~6.5 m (banda 6.0–7.0) → **Emergência**
- **B) DC-RS Dom Tito:** baseline 3.83 m · pico v1.0 ~6.4 m (banda 5.9–6.9) → **Alerta**
- **Δ pico (B − A): -0.10 m** · ⚠ MUDA A CLASSE: Emergência → Alerta
- nível atual: SDC 5.81 m · DC-RS 5.64 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.49 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
