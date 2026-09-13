# Cheia — Rio do Sul (SC) — 2026-09-13 08:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.6 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.77 m · DC-RS Dom Tito: 5.6 m · offset medido DC-RS−SDC: -0.17 m
**Chuva 24h máx (drivers):** 2.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.61 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.017 m/h (anterior -0.01 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~5.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.6 m (banda p10–p90 5.1–6.1 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.47 m em 12/09 18:19 (DC-RS) · subida até agora 0.13 m
- chuva-jusante do ato: 0.5 mm (drivers (divergiu +11% das ancoras); soma horária desde o vale (14 h, cobertura 99%)) · chuva-acima 1.7 mm
- cj efetiva 6 mm = cj 1 + trânsito-acima 0 (fração de comportas aberta 0.20) + pluviômetro-ΔV 5 (ΔV do ato 7.2 hm³)
- sombra (cj_lat, c/ laterais): ~5.6 m (cj 0 mm · Δcj_lat−cj_v07 = -0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.7 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 55.44 → 62.63 | 7.2 | 0.00 | 0A/7F | 18.93 m |  |
| Sul | 21.37 → 21.04 | 0.0 | 0.40 | 2A/3F | 19.61 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (14 h, cobertura 99%)

| Município | Chuva do ato (mm) |
|---|---|
| Salete | 2.4 |
| Rio do Oeste | 1.4 |
| Rio do Sul | 1.1 |
| Taio | 0.2 |
| Agronomica | 0.2 |
| Trombudo Central | 0.1 |
| Ituporanga | 0.0 |
| Aurora | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 4.2, Rio do Campo 0.8, Alfredo Wagner 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 62.63 | 0A/7F | 0 | 18.93 m | 13/09 08:26 |
| Barragem Sul Ituporanga | 21.04 | 2A/3F | 0 | 19.61 m | 13/09 08:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.17 m** · fallback -0.16 m
- **A) SDC-00013:** baseline 5.63 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.47 m · pico v1.0 ~5.6 m (banda 5.1–6.1) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.77 m · DC-RS 5.6 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.77 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
