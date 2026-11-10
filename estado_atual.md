# Cheia — Rio do Sul (SC) — 2026-11-10 13:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.84 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 6.08 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.85 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.039 m/h (anterior -0.058 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~6.2 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.2 m (banda p10–p90 5.4–6.8 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.83 m em 10/11 13:09 (DC-RS) · subida até agora 0.01 m
- chuva-jusante do ato: 0.2 mm (drivers (divergiu -56% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.1 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³) · **VERTENDO** (+0.37 m)
- sombra (cj_lat, c/ laterais): ~6.2 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.3 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 81.85 → 81.76 | 0.0 | 0.00 | 0A/7F | 21.25 m |  |
| Sul | 106.83 → 106.73 | 0.0 | 0.00 | 0A/5F | 31.67 m | vertendo |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Ituporanga | 1.2 |
| Aurora | 0.6 |
| Trombudo Central | 0.2 |
| Taio | 0.1 |
| Rio do Sul | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 0.4, Alfredo Wagner 0.0, Rio do Campo 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 81.76 | 0A/7F | 0 | 21.25 m | 10/11 13:26 |
| Barragem Sul Ituporanga | 106.73 | 0A/5F | 0.670013427734375 | 31.67 m | 10/11 13:26 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 6.07 m · pico v1.0 ~6.4 m (banda 5.7–7.1) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.83 m · pico v1.0 ~6.2 m (banda 5.4–6.8) → **Alerta**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 6.08 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
