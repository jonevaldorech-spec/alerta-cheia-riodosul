# Cheia — Rio do Sul (SC) — 2026-11-27 01:03 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 6.02 m — **ALERTA** · tendência subindo
- SDC-00013: 6.07 m · DC-RS Dom Tito: 6.02 m · offset medido DC-RS−SDC: -0.05 m
**Chuva 24h máx (drivers):** 0.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~6.02 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.003 m/h (anterior 0.0 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~5.1 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.1 m (banda p10–p90 4.6–5.6 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.12 m em 25/11 15:43 (DC-RS) · subida até agora 0.9 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu -32% das ancoras); soma horária desde o vale (35 h, cobertura 100%)) · chuva-acima 0.2 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.74) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.1 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.4 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 38.74 → 34.0 | 0.0 | 0.71 | 7A/1F | 15.0 m |  |
| Sul | 44.04 → 29.97 | 0.0 | 0.77 | 5A/1F | 21.56 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (35 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.4 |
| Agrolandia | 0.4 |
| Rio do Oeste | 0.2 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 0.8, Alfredo Wagner 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 34.0 | 7A/1F | 0 | 15.0 m | 27/11 00:55 |
| Barragem Sul Ituporanga | 29.97 | 5A/1F | 0 | 21.56 m | 27/11 00:55 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.05 m** · fallback -0.2 m
- **A) SDC-00013:** baseline 5.32 m · pico v1.0 ~5.3 m (banda 4.8–5.8) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 5.12 m · pico v1.0 ~5.1 m (banda 4.6–5.6) → **Atenção**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 6.07 m · DC-RS 6.02 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 ()
