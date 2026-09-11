# Cheia — Rio do Sul (SC) — 2026-09-10 21:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.13 m — **Normal** · tendência estável/caindo
- SDC-00013: 4.29 m · DC-RS Dom Tito: 4.13 m · offset medido DC-RS−SDC: -0.16 m
**Chuva 24h máx (drivers):** 83.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.14 m → **Normal** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.056 m/h (anterior -0.018 m/h) · chuva-driver 2h 1.7 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~4.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~4.6 m (banda p10–p90 4.1–5.1 m) → **Atenção**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.93 m em 09/09 23:09 (DC-RS) · subida até agora 1.2 m
- chuva-jusante do ato: 39.5 mm (drivers (divergiu -20% das ancoras); soma horária desde o vale (23 h, cobertura 100%)) · chuva-acima 39.6 mm
- cj efetiva 52 mm = cj 39 + trânsito-acima 12 (fração de comportas aberta 0.72) + pluviômetro-ΔV 0 (ΔV do ato 0.6 hm³)
- sombra (cj_lat, c/ laterais): ~4.5 m (cj 36 mm · Δcj_lat−cj_v07 = -3.5 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.2 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 41.84 → 11.35 | 0.0 | 0.82 | 0A/7F | 10.97 m |  |
| Sul | 0.0 → 0.58 | 0.6 | 0.63 | 0A/5F | 9.5 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (23 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Taio | 66.4 |
| Rio do Sul | 52.5 |
| Pouso Redondo | 42.7 |
| Salete | 38.0 |
| Rio do Oeste | 37.4 |
| Trombudo Central | 35.9 |
| Laurentino | 35.6 |
| Aurora | 34.7 |
| Agrolandia | 34.3 |
| Ituporanga | 29.1 |
| Agronomica | 27.6 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 50.0, Rio do Campo 44.2, Alfredo Wagner 24.7

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 11.35 | 0A/7F | 0 | 10.97 m |
| Barragem Sul Ituporanga | 0.58 | 0A/5F | 0 | 9.5 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.16 m** · fallback -0.14 m
- **A) SDC-00013:** baseline 3.07 m · pico v1.0 ~4.8 m (banda 4.3–5.3) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 2.93 m · pico v1.0 ~4.6 m (banda 4.1–5.1) → **Atenção**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 4.29 m · DC-RS 4.13 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.02 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
