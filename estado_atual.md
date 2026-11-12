# Cheia — Rio do Sul (SC) — 2026-11-12 04:00 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.6 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.84 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.61 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.01 m/h (anterior 0.007 m/h) · chuva-driver 2h 0.1 mm/h
- réguas-líder: Pouso Redondo: subindo · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.4 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.4 m (banda p10–p90 4.9–5.9 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.39 m em 11/11 14:32 (DC-RS) · subida até agora 0.21 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu +64% das ancoras); soma horária desde o vale (14 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.4 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.7 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 72.57 → 65.98 | 0.0 | 1.00 | 7A/0F | 19.35 m |  |
| Sul | 93.25 → 84.49 | 0.0 | 1.00 | 5A/0F | 29.34 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (14 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Oeste | 1.0 |
| Rio do Sul | 0.2 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.0, Rio do Campo 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 65.98 | 7A/0F | 0 | 19.35 m | 12/11 03:57 |
| Barragem Sul Ituporanga | 84.49 | 5A/0F | 0 | 29.34 m | 12/11 03:56 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 5.63 m · pico v1.0 ~5.6 m (banda 5.1–6.1) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.39 m · pico v1.0 ~5.4 m (banda 4.9–5.9) → **Atenção**
- **Δ pico (B − A): -0.20 m** · ⚠ MUDA A CLASSE: Alerta → Atenção
- nível atual: SDC 5.84 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
