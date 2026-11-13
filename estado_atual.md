# Cheia — Rio do Sul (SC) — 2026-11-13 05:00 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.69 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.93 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 35.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.69 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.013 m/h (anterior -0.016 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: subindo · Agrolandia: virou
- o v1.0 vira **TETO** (~5.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.6 m (banda p10–p90 5.1–6.1 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.39 m em 11/11 14:32 (DC-RS) · subida até agora 0.3 m
- chuva-jusante do ato: 7.2 mm (drivers (divergiu -40% das ancoras); soma horária desde o vale (39 h, cobertura 100%)) · chuva-acima 0.8 mm
- cj efetiva 8 mm = cj 7 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.6 m (cj 6 mm · Δcj_lat−cj_v07 = -1.7 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.9 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 72.57 → 53.85 | 0.0 | 1.00 | 7A/0F | 17.79 m |  |
| Sul | 93.25 → 68.36 | 0.0 | 1.00 | 5A/0F | 27.43 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (39 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 35.9 |
| Pouso Redondo | 21.4 |
| Rio do Oeste | 15.0 |
| Aurora | 5.3 |
| Trombudo Central | 1.2 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Salete | 0.0 |
| Laurentino | 0.0 |
| Agrolandia | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 2.2, Taio_montante 0.2, Rio do Campo 0.1

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 53.85 | 7A/0F | 0 | 17.79 m | 13/11 04:56 |
| Barragem Sul Ituporanga | 68.36 | 5A/0F | 0 | 27.43 m | 13/11 04:56 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 5.63 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.39 m · pico v1.0 ~5.6 m (banda 5.1–6.1) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.93 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
