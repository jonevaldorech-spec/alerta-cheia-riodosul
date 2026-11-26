# Cheia — Rio do Sul (SC) — 2026-11-26 06:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.87 m — **ALERTA** · tendência subindo
- SDC-00013: 5.97 m · DC-RS Dom Tito: 5.87 m · offset medido DC-RS−SDC: -0.1 m
**Chuva 24h máx (drivers):** 0.5 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.87 m → **ALERTA** · crista em ~0 h
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.054 m/h (anterior 0.076 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~5.1 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.1 m (banda p10–p90 4.6–5.6 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.12 m em 25/11 15:43 (DC-RS) · subida até agora 0.75 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -18% das ancoras); soma horária desde o vale (16 h, cobertura 100%)) · chuva-acima 0.5 mm
- cj efetiva 1 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.60) + pluviômetro-ΔV 0 (ΔV do ato 0.5 hm³)
- sombra (cj_lat, c/ laterais): ~5.1 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.4 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 38.74 → 39.29 | 0.5 | 0.51 | 5A/3F | 15.78 m |  |
| Sul | 44.04 → 39.98 | 0.0 | 0.69 | 5A/1F | 23.37 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (16 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Agrolandia | 0.2 |
| Rio do Sul | 0.1 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 1.5, Alfredo Wagner 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 39.29 | 5A/3F | 0 | 15.78 m | 26/11 06:25 |
| Barragem Sul Ituporanga | 39.98 | 5A/1F | 0 | 23.37 m | 26/11 06:25 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.1 m** · fallback -0.22 m
- **A) SDC-00013:** baseline 5.34 m · pico v1.0 ~5.4 m (banda 4.9–5.9) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 5.12 m · pico v1.0 ~5.1 m (banda 4.6–5.6) → **Atenção**
- **Δ pico (B − A): -0.30 m** · classe inalterada
- nível atual: SDC 5.97 m · DC-RS 5.87 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (), 00125 (Rio do Campo (H))
