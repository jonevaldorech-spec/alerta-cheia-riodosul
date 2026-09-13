# Cheia — Rio do Sul (SC) — 2026-09-13 13:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.5 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.66 m · DC-RS Dom Tito: 5.5 m · offset medido DC-RS−SDC: -0.16 m
**Chuva 24h máx (drivers):** 2.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.5 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.021 m/h (anterior -0.022 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.7 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.7 m (banda p10–p90 5.2–6.2 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.47 m em 12/09 18:19 (DC-RS) · subida até agora 0.03 m
- chuva-jusante do ato: 0.5 mm (drivers (divergiu +11% das ancoras); soma horária desde o vale (19 h, cobertura 99%)) · chuva-acima 1.7 mm
- cj efetiva 7 mm = cj 1 + trânsito-acima 0 (fração de comportas aberta 0.20) + pluviômetro-ΔV 6 (ΔV do ato 9.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.7 m (cj 0 mm · Δcj_lat−cj_v07 = -0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.7 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 55.44 → 64.47 | 9.0 | 0.00 | 0A/7F | 19.16 m |  |
| Sul | 21.37 → 20.67 | 0.0 | 0.40 | 2A/3F | 19.54 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (19 h, cobertura 99%)

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
| Barragem Oeste Taió | 64.47 | 0A/7F | 0 | 19.16 m | 13/09 13:26 |
| Barragem Sul Ituporanga | 20.67 | 2A/3F | 0 | 19.54 m | 13/09 13:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.16 m** · fallback -0.17 m
- **A) SDC-00013:** baseline 5.64 m · pico v1.0 ~5.8 m (banda 5.3–6.3) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.47 m · pico v1.0 ~5.7 m (banda 5.2–6.2) → **Alerta**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 5.66 m · DC-RS 5.5 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.69 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
