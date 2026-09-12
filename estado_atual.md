# Cheia — Rio do Sul (SC) — 2026-09-11 22:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.87 m — **ALERTA** · tendência subindo
- SDC-00013: 6.03 m · DC-RS Dom Tito: 5.87 m · offset medido DC-RS−SDC: -0.16 m
**Chuva 24h máx (drivers):** 82.2 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.87 m → **ALERTA** · crista em ~0 h
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.062 m/h (anterior 0.136 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.8 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.8 m (banda p10–p90 5.3–6.3 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 3.83 m em 11/09 06:42 (DC-RS) · subida até agora 2.04 m
- chuva-jusante do ato: 49.8 mm (ancoras; soma horária desde o vale (16 h, cobertura 100%)) · chuva-acima 60.8 mm
- cj efetiva 66 mm = cj 50 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 16 (ΔV do ato 23.2 hm³)
- sombra (cj_lat, c/ laterais): ~5.6 m (cj 41 mm · Δcj_lat−cj_v07 = -5.8 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.6 m → Emergência (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 14.87 → 30.63 | 15.8 | 0.00 | 0A/7F | 14.48 m |  |
| Sul | 0.58 → 7.72 | 7.4 | 0.00 | 0A/5F | 15.5 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (16 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Salete | 94.0 |
| Rio do Sul | 67.0 |
| Taio | 53.0 |
| Trombudo Central | 43.1 |
| Rio do Oeste | 42.4 |
| Laurentino | 41.4 |
| Pouso Redondo | 36.8 |
| Aurora | 36.6 |
| Agronomica | 36.2 |
| Agrolandia | 32.4 |
| Ituporanga | 29.4 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 92.2, Taio_montante 60.4, Alfredo Wagner 29.8

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 30.63 | 0A/7F | 0 | 14.48 m | 11/09 22:26 |
| Barragem Sul Ituporanga | 7.72 | 0A/5F | 0 | 15.5 m | 11/09 22:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.16 m** · fallback -0.14 m
- **A) SDC-00013:** baseline 3.97 m · pico v1.0 ~5.9 m (banda 5.4–6.4) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 3.83 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 6.03 m · DC-RS 5.87 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 5.6 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
