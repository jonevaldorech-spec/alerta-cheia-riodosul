# Cheia — Rio do Sul (SC) — 2026-11-16 00:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.55 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.79 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 44.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.65 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.007 m/h (anterior 0.02 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.8 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.8 m (banda p10–p90 5.3–6.3 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.16 m em 15/11 15:45 (DC-RS) · subida até agora 0.39 m
- chuva-jusante do ato: 18.3 mm (drivers (divergiu -37% das ancoras); soma horária desde o vale (9 h, cobertura 100%)) · chuva-acima 11.1 mm
- cj efetiva 23 mm = cj 18 + trânsito-acima 4 (fração de comportas aberta 0.95) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.7 m (cj 16 mm · Δcj_lat−cj_v07 = -2.2 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.2 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 24.75 → 22.28 | 0.0 | 1.00 | 8A/0F | 13.11 m |  |
| Sul | 30.23 → 24.42 | 0.0 | 0.90 | 6A/0F | 20.37 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (9 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Taio | 47.5 |
| Rio do Sul | 24.6 |
| Pouso Redondo | 21.8 |
| Aurora | 20.5 |
| Agrolandia | 17.8 |
| Agronomica | 17.2 |
| Ituporanga | 15.7 |
| Rio do Oeste | 10.2 |
| Salete | 9.4 |
| Laurentino | 9.4 |
| Trombudo Central | 7.7 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 19.0, Taio_montante 13.0, Alfredo Wagner 1.4

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 22.28 | 8A/0F | 0 | 13.11 m | 16/11 00:26 |
| Barragem Sul Ituporanga | 24.42 | 6A/0F | 0 | 20.37 m | 16/11 00:27 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 5.4 m · pico v1.0 ~6.0 m (banda 5.5–6.5) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.16 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.79 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
