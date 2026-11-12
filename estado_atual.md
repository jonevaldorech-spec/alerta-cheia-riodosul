# Cheia — Rio do Sul (SC) — 2026-11-12 14:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.63 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.87 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.0 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.63 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.003 m/h (anterior 0.003 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: subindo · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.4 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.4 m (banda p10–p90 4.9–5.9 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.39 m em 11/11 14:32 (DC-RS) · subida até agora 0.24 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu +45% das ancoras); soma horária desde o vale (24 h, cobertura 100%)) · chuva-acima 0.6 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.4 m (cj 0 mm · Δcj_lat−cj_v07 = 0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.6 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 72.57 → 60.8 | 0.0 | 1.00 | 7A/0F | 18.7 m |  |
| Sul | 93.25 → 77.68 | 0.0 | 1.00 | 5A/0F | 28.57 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (24 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Oeste | 1.0 |
| Rio do Sul | 0.3 |
| Pouso Redondo | 0.2 |
| Aurora | 0.1 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Salete | 0.0 |
| Laurentino | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 1.6, Taio_montante 0.2, Rio do Campo 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 60.8 | 7A/0F | 0 | 18.7 m | 12/11 14:26 |
| Barragem Sul Ituporanga | 77.68 | 5A/0F | 0 | 28.57 m | 12/11 14:27 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 5.63 m · pico v1.0 ~5.6 m (banda 5.2–6.1) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.39 m · pico v1.0 ~5.4 m (banda 4.9–5.9) → **Atenção**
- **Δ pico (B − A): -0.20 m** · ⚠ MUDA A CLASSE: Alerta → Atenção
- nível atual: SDC 5.87 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
