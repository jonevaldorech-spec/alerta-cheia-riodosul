# Cheia — Rio do Sul (SC) — 2026-11-27 10:43 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.74 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.97 m · DC-RS Dom Tito: 5.74 m · offset medido DC-RS−SDC: -0.23 m
**Chuva 24h máx (drivers):** 0.3 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.77 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.047 m/h (anterior -0.088 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.7 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.7 m (banda p10–p90 5.3–6.2 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.74 m em 27/11 10:38 (DC-RS) · subida até agora 0.0 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -73% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.1 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.85) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.7 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.9 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 31.02 → 30.69 | 0.0 | 0.87 | 7A/1F | 14.49 m |  |
| Sul | 25.27 → 24.73 | 0.0 | 0.83 | 5A/1F | 20.46 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.1 |
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

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 0.5, Alfredo Wagner 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 30.69 | 7A/1F | 0 | 14.49 m | 27/11 10:35 |
| Barragem Sul Ituporanga | 24.73 | 5A/1F | 0 | 20.46 m | 27/11 10:35 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.23 m** · fallback -0.145 m
- **A) SDC-00013:** baseline 5.88 m · pico v1.0 ~5.9 m (banda 5.4–6.4) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.74 m · pico v1.0 ~5.7 m (banda 5.3–6.2) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.97 m · DC-RS 5.74 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 ()
