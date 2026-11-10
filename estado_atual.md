# Cheia — Rio do Sul (SC) — 2026-11-10 11:00 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.94 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 6.18 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.4 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.97 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.056 m/h (anterior -0.062 m/h) · chuva-driver 2h 1.4 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~6.3 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~6.3 m (banda p10–p90 5.6–7.0 m) → **Alerta**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.96 m em 10/11 10:58 (DC-RS) · subida até agora -0.02 m
- chuva-jusante do ato: 0.2 mm (drivers (divergiu -54% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.3 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.08) + pluviômetro-ΔV 0 (ΔV do ato 0.1 hm³) · **VERTENDO** (+0.37 m)
- sombra (cj_lat, c/ laterais): ~6.3 m (cj 0 mm · Δcj_lat−cj_v07 = 0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~6.4 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 81.85 → 81.94 | 0.1 | 0.00 | 0A/7F | 21.27 m |  |
| Sul | 107.64 → 107.44 | 0.0 | 0.16 | 0A/5F | 31.74 m | vertendo |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Ituporanga | 1.2 |
| Aurora | 0.7 |
| Taio | 0.3 |
| Salete | 0.2 |
| Trombudo Central | 0.2 |
| Rio do Sul | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 0.5, Taio_montante 0.4, Rio do Campo 0.1

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 81.94 | 0A/7F | 0 | 21.27 m | 10/11 10:57 |
| Barragem Sul Ituporanga | 107.44 | 0A/5F | 0.739990234375 | 31.74 m | 10/11 10:56 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 6.2 m · pico v1.0 ~6.6 m (banda 5.8–7.2) → **Emergência**
- **B) DC-RS Dom Tito:** baseline 5.96 m · pico v1.0 ~6.3 m (banda 5.6–7.0) → **Alerta**
- **Δ pico (B − A): -0.30 m** · ⚠ MUDA A CLASSE: Emergência → Alerta
- nível atual: SDC 6.18 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
