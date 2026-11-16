# Cheia — Rio do Sul (SC) — 2026-11-16 13:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.24)):** 5.57 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.81 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 42.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.57 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.046 m/h (anterior -0.035 m/h) · chuva-driver 2h 0.2 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~5.4 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.4 m (banda p10–p90 4.9–5.9 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.41 m em 16/11 13:29 (DC-RS) · subida até agora 0.16 m
- chuva-jusante do ato: 0.1 mm (drivers (divergiu -18% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.4 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.4 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.6 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 18.22 → 18.06 | 0.0 | 1.00 | 8A/0F | 12.35 m |  |
| Sul | 19.03 → 19.03 | 0.0 | 1.00 | 6A/0F | 19.13 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.2 |
| Agrolandia | 0.2 |
| Agronomica | 0.2 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Trombudo Central | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Alfredo Wagner 1.0, Taio_montante 0.2, Rio do Campo 0.1

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 18.06 | 8A/0F | 0 | 12.35 m | 16/11 13:26 |
| Barragem Sul Ituporanga | 19.03 | 6A/0F | 0 | 19.13 m | 16/11 13:27 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.24)** · offset medido DC-RS−SDC: **None m** · fallback -0.24 m
- **A) SDC-00013:** baseline 5.65 m · pico v1.0 ~5.7 m (banda 5.2–6.2) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.41 m · pico v1.0 ~5.4 m (banda 4.9–5.9) → **Atenção**
- **Δ pico (B − A): -0.30 m** · ⚠ MUDA A CLASSE: Alerta → Atenção
- nível atual: SDC 5.81 m · DC-RS None m

## ⚠ Avisos desta coleta

- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 ()
