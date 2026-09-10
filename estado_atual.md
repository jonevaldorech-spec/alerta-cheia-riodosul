# Cheia — Rio do Sul (SC) — 2026-09-10 20:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.19 m — **Normal** · tendência estável/caindo
- SDC-00013: 4.35 m · DC-RS Dom Tito: 4.19 m · offset medido DC-RS−SDC: -0.16 m
**Chuva 24h máx (drivers):** 83.7 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.2 m → **Normal** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.046 m/h (anterior 0.006 m/h) · chuva-driver 2h 1.7 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~4.7 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~4.7 m (banda p10–p90 4.2–5.2 m) → **Atenção**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.93 m em 09/09 23:09 (DC-RS) · subida até agora 1.26 m
- chuva-jusante do ato: 39.5 mm (drivers (divergiu -20% das ancoras); soma horária desde o vale (22 h, cobertura 100%)) · chuva-acima 39.9 mm
- cj efetiva 53 mm = cj 39 + trânsito-acima 13 (fração de comportas aberta 0.76) + pluviômetro-ΔV 0 (ΔV do ato 0.6 hm³)
- sombra (cj_lat, c/ laterais): ~4.5 m (cj 36 mm · Δcj_lat−cj_v07 = -3.6 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.2 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 41.84 → 10.82 | 0.0 | 0.86 | 0A/7F | 10.85 m |  |
| Sul | 0.0 → 0.58 | 0.6 | 0.66 | 0A/5F | 9.5 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (22 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Taio | 67.2 |
| Rio do Sul | 52.5 |
| Pouso Redondo | 42.7 |
| Salete | 38.8 |
| Rio do Oeste | 37.2 |
| Trombudo Central | 35.8 |
| Laurentino | 35.4 |
| Aurora | 34.5 |
| Agrolandia | 33.8 |
| Ituporanga | 28.9 |
| Agronomica | 27.6 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 50.4, Rio do Campo 45.2, Alfredo Wagner 24.1

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 10.82 | 0A/7F | 0 | 10.85 m |
| Barragem Sul Ituporanga | 0.58 | 0A/5F | 0 | 9.5 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.16 m** · fallback -0.14 m
- **A) SDC-00013:** baseline 3.07 m · pico v1.0 ~4.8 m (banda 4.3–5.3) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 2.93 m · pico v1.0 ~4.7 m (banda 4.2–5.2) → **Atenção**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.35 m · DC-RS 4.19 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.22 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
