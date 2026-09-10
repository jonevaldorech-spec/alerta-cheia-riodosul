# Cheia — Rio do Sul (SC) — 2026-09-10 18:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.28 m — **Normal** · tendência estável/caindo
- SDC-00013: 4.42 m · DC-RS Dom Tito: 4.28 m · offset medido DC-RS−SDC: -0.14 m
**Chuva 24h máx (drivers):** 83.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.28 m → **Normal** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.006 m/h (anterior 0.033 m/h) · chuva-driver 2h 0.6 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~4.7 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~4.7 m (banda p10–p90 4.2–5.2 m) → **Atenção**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.93 m em 09/09 23:09 (DC-RS) · subida até agora 1.35 m
- chuva-jusante do ato: 38.9 mm (drivers (divergiu -20% das ancoras); soma horária desde o vale (20 h, cobertura 100%)) · chuva-acima 38.1 mm
- cj efetiva 53 mm = cj 39 + trânsito-acima 13 (fração de comportas aberta 0.84) + pluviômetro-ΔV 0 (ΔV do ato 0.6 hm³)
- sombra (cj_lat, c/ laterais): ~4.6 m (cj 35 mm · Δcj_lat−cj_v07 = -3.5 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.2 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 41.84 → 9.61 | 0.0 | 0.95 | 0A/7F | 10.56 m |  |
| Sul | 0.0 → 0.58 | 0.6 | 0.73 | 0A/5F | 9.5 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (20 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Taio | 64.8 |
| Rio do Sul | 51.5 |
| Pouso Redondo | 42.7 |
| Rio do Oeste | 37.0 |
| Salete | 36.8 |
| Trombudo Central | 35.2 |
| Laurentino | 35.2 |
| Aurora | 34.4 |
| Agrolandia | 33.8 |
| Ituporanga | 28.9 |
| Agronomica | 27.2 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 48.8, Rio do Campo 41.5, Alfredo Wagner 23.9

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 9.61 | 0A/7F | 0 | 10.56 m |
| Barragem Sul Ituporanga | 0.58 | 0A/5F | 0 | 9.5 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.14 m** · fallback -0.14 m
- **A) SDC-00013:** baseline 3.07 m · pico v1.0 ~4.8 m (banda 4.3–5.3) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 2.93 m · pico v1.0 ~4.7 m (banda 4.2–5.2) → **Atenção**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.42 m · DC-RS 4.28 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.75 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
