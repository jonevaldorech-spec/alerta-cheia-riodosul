# Cheia — Rio do Sul (SC) — 2026-11-27 19:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.67 m — **ALERTA** · tendência subindo
- SDC-00013: 5.85 m · DC-RS Dom Tito: 5.67 m · offset medido DC-RS−SDC: -0.18 m
**Chuva 24h máx (drivers):** 0.3 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.67 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.016 m/h (anterior 0.012 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: subindo · Agrolandia: virou
- o v1.0 vira **TETO** (~5.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.6 m (banda p10–p90 5.1–6.1 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.61 m em 27/11 14:53 (DC-RS) · subida até agora 0.06 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu +64% das ancoras); soma horária desde o vale (5 h, cobertura 100%)) · chuva-acima 0.4 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.39) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.6 m (cj 0 mm · Δcj_lat−cj_v07 = -0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.8 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 29.59 → 28.77 | 0.0 | 0.45 | 0A/8F | 14.19 m |  |
| Sul | 23.16 → 21.74 | 0.0 | 0.32 | 0A/6F | 19.79 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (5 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Salete | 0.2 |
| Pouso Redondo | 0.2 |
| Taio | 0.1 |
| Trombudo Central | 0.1 |
| Rio do Sul | 0.0 |
| Ituporanga | 0.0 |
| Aurora | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Agrolandia | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 0.9, Taio_montante 0.2, Alfredo Wagner 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 28.77 | 0A/8F | 0 | 14.19 m | 27/11 18:55 |
| Barragem Sul Ituporanga | 21.74 | 0A/6F | 0 | 19.79 m | 27/11 18:55 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.18 m** · fallback -0.145 m
- **A) SDC-00013:** baseline 5.75 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.61 m · pico v1.0 ~5.6 m (banda 5.1–6.1) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.85 m · DC-RS 5.67 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 ()
