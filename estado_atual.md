# Cheia — Rio do Sul (SC) — 2026-09-12 16:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.51 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.68 m · DC-RS Dom Tito: 5.51 m · offset medido DC-RS−SDC: -0.17 m
**Chuva 24h máx (drivers):** 14.0 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.52 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.031 m/h (anterior -0.023 m/h) · chuva-driver 2h 0.1 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.5 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.5 m (banda p10–p90 5.0–6.0 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.5 m em 12/09 16:29 (DC-RS) · subida até agora 0.01 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -59% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.20) + pluviômetro-ΔV 0 (ΔV do ato 0.5 hm³)
- sombra (cj_lat, c/ laterais): ~5.5 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.7 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 53.77 → 54.23 | 0.5 | 0.00 | 0A/7F | 17.84 m |  |
| Sul | 21.37 → 21.37 | 0.0 | 0.40 | 2A/3F | 19.7 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.1 |
| Aurora | 0.1 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.0, Rio do Campo 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 54.23 | 0A/7F | 0 | 17.84 m | 12/09 16:26 |
| Barragem Sul Ituporanga | 21.37 | 2A/3F | 0 | 19.7 m | 12/09 16:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.17 m** · fallback -0.16 m
- **A) SDC-00013:** baseline 5.66 m · pico v1.0 ~5.7 m (banda 5.2–6.2) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.5 m · pico v1.0 ~5.5 m (banda 5.0–6.0) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 5.68 m · DC-RS 5.51 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.24 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
