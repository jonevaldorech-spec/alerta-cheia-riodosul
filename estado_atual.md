# Cheia — Rio do Sul (SC) — 2026-11-27 22:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.56 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.65 m · DC-RS Dom Tito: 5.56 m · offset medido DC-RS−SDC: -0.09 m
**Chuva 24h máx (drivers):** 3.5 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.57 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.077 m/h (anterior 0.03 m/h) · chuva-driver 2h 1.7 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: subindo · Agrolandia: virou
- o v1.0 vira **TETO** (~5.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.6 m (banda p10–p90 5.1–6.1 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.56 m em 27/11 21:59 (DC-RS) · subida até agora 0.0 m
- chuva-jusante do ato: 1.5 mm (drivers (divergiu -26% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 0 h, cobertura 0%)) · chuva-acima 1.9 mm
- cj efetiva 2 mm = cj 2 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 0 (ΔV do ato 0.3 hm³)
- sombra (cj_lat, c/ laterais): ~5.6 m (cj 1 mm · Δcj_lat−cj_v07 = -0.2 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.8 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 29.14 → 29.27 | 0.1 | 0.00 | 0A/8F | 14.27 m |  |
| Sul | 22.0 → 22.18 | 0.2 | 0.00 | 0A/6F | 19.89 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 0 h, cobertura 0%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 3.3 |
| Salete | 2.8 |
| Taio | 2.1 |
| Aurora | 1.8 |
| Pouso Redondo | 1.4 |
| Trombudo Central | 1.2 |
| Rio do Oeste | 1.2 |
| Agronomica | 1.2 |
| Ituporanga | 0.8 |
| Agrolandia | 0.8 |
| Laurentino | 0.2 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 3.5, Taio_montante 2.0, Alfredo Wagner 0.3

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 29.27 | 0A/8F | 0 | 14.27 m | 27/11 21:55 |
| Barragem Sul Ituporanga | 22.18 | 0A/6F | 0 | 19.89 m | 27/11 21:55 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.09 m** · fallback -0.14 m
- **A) SDC-00013:** baseline 5.7 m · pico v1.0 ~5.7 m (banda 5.3–6.2) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.56 m · pico v1.0 ~5.6 m (banda 5.1–6.1) → **Alerta**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 5.65 m · DC-RS 5.56 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 ()
