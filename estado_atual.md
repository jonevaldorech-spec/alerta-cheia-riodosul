# Cheia — Rio do Sul (SC) — 2026-11-25 18:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.16 m — **ATENÇÃO** · tendência subindo
- SDC-00013: 5.45 m · DC-RS Dom Tito: 5.16 m · offset medido DC-RS−SDC: -0.29 m
**Chuva 24h máx (drivers):** 5.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.16 m → **ATENÇÃO** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.019 m/h (anterior -0.03 m/h) · chuva-driver 2h 0.1 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.1 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.1 m (banda p10–p90 4.7–5.6 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ATENÇÃO**
- baseline = VALE do ato: 5.12 m em 25/11 15:43 (DC-RS) · subida até agora 0.04 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -73% das ancoras); soma horária desde o vale (4 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 1 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.30) + pluviômetro-ΔV 1 (ΔV do ato 1.4 hm³)
- sombra (cj_lat, c/ laterais): ~5.1 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.4 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 38.74 → 39.77 | 1.0 | 0.26 | 3A/5F | 15.85 m |  |
| Sul | 44.04 → 44.4 | 0.4 | 0.35 | 3A/3F | 24.09 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (4 h, cobertura 100%)

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

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.0, Rio do Campo 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 39.77 | 3A/5F | 0 | 15.85 m | 25/11 18:25 |
| Barragem Sul Ituporanga | 44.4 | 3A/3F | 0 | 24.09 m | 25/11 18:25 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.29 m** · fallback -0.25 m
- **A) SDC-00013:** baseline 5.37 m · pico v1.0 ~5.4 m (banda 4.9–5.9) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 5.12 m · pico v1.0 ~5.1 m (banda 4.7–5.6) → **Atenção**
- **Δ pico (B − A): -0.30 m** · classe inalterada
- nível atual: SDC 5.45 m · DC-RS 5.16 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (), 00066 (SDC-SC Taio (H))
