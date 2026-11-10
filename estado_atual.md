# Cheia — Rio do Sul (SC) — 2026-11-10 09:00 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 6.05 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 6.29 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.0 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~6.07 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.067 m/h (anterior -0.052 m/h) · chuva-driver 2h 1.0 mm/h
- réguas-líder: Pouso Redondo: subindo · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~6.4 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.4 m (banda p10–p90 5.7–7.1 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 6.06 m em 10/11 08:59 (DC-RS) · subida até agora -0.01 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu -14% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.3 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.10) + pluviômetro-ΔV 0 (ΔV do ato 0.1 hm³) · **VERTENDO** (+0.37 m)
- sombra (cj_lat, c/ laterais): ~6.4 m (cj 0 mm · Δcj_lat−cj_v07 = 0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.5 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 81.5 → 81.59 | 0.1 | 0.00 | 0A/7F | 21.23 m |  |
| Sul | 107.84 → 107.84 | 0.0 | 0.20 | 1A/4F | 31.78 m | vertendo |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Aurora | 0.6 |
| Taio | 0.3 |
| Salete | 0.2 |
| Rio do Sul | 0.0 |
| Ituporanga | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.5, Taio_montante 0.4, Rio do Campo 0.1

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 81.59 | 0A/7F | 0 | 21.23 m | 10/11 08:56 |
| Barragem Sul Ituporanga | 107.84 | 1A/4F | 0.779998779296875 | 31.78 m | 10/11 08:57 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 6.3 m · pico v1.0 ~6.7 m (banda 5.9–7.3) → **Emergência**
- **B) DC-RS Dom Tito:** baseline 6.06 m · pico v1.0 ~6.4 m (banda 5.7–7.1) → **Alerta**
- **Δ pico (B − A): -0.30 m** · ⚠ MUDA A CLASSE: Emergência → Alerta
- nível atual: SDC 6.29 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
