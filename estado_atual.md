# Cheia — Rio do Sul (SC) — 2026-11-25 14:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.22 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 5.56 m · DC-RS Dom Tito: 5.22 m · offset medido DC-RS−SDC: -0.34 m
**Chuva 24h máx (drivers):** 61.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.22 m → **ATENÇÃO** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.004 m/h (anterior -0.049 m/h) · chuva-driver 2h 0.1 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.2 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.2 m (banda p10–p90 4.8–5.7 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ATENÇÃO**
- baseline = VALE do ato: 5.22 m em 25/11 12:12 (DC-RS) · subida até agora 0.0 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -73% das ancoras); soma horária desde o vale (2 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 1 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.15) + pluviômetro-ΔV 1 (ΔV do ato 1.1 hm³)
- sombra (cj_lat, c/ laterais): ~5.2 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.4 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 37.72 → 38.33 | 0.6 | 0.12 | 1A/7F | 15.64 m |  |
| Sul | 43.6 → 44.04 | 0.5 | 0.17 | 1A/5F | 24.03 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (2 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.2 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.0, Rio do Campo 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 38.33 | 1A/7F | 0 | 15.64 m | 25/11 13:55 |
| Barragem Sul Ituporanga | 44.04 | 1A/5F | 0 | 24.03 m | 25/11 13:55 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.34 m** · fallback -0.23 m
- **A) SDC-00013:** baseline 5.45 m · pico v1.0 ~5.5 m (banda 5.0–6.0) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 5.22 m · pico v1.0 ~5.2 m (banda 4.8–5.7) → **Atenção**
- **Δ pico (B − A): -0.30 m** · classe inalterada
- nível atual: SDC 5.56 m · DC-RS 5.22 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (), 00035 (SDC-SC Trombudo Central 2)
