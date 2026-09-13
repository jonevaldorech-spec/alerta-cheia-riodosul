# Cheia — Rio do Sul (SC) — 2026-09-13 01:30 (local −03)

**Rio do Sul (SDC+offset (DC-RS indisponível, off=-0.16)):** 5.66 m — **ALERTA** · tendência estável/caindo
- SDC-00013: 5.82 m · DC-RS Dom Tito: None m · offset medido DC-RS−SDC: None m · ⚠ DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
**Chuva 24h máx (drivers):** 1.6 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.66 m → **ALERTA** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.01 m/h (anterior 0.03 m/h) · chuva-driver 2h 1.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~5.5 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.5 m (banda p10–p90 5.0–6.0 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ALERTA**
- baseline = VALE do ato: 5.47 m em 12/09 18:19 (DC-RS) · subida até agora 0.19 m
- chuva-jusante do ato: 0.3 mm (ancoras; soma horária desde o vale (8 h, cobertura 100%)) · chuva-acima 0.3 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.50) + pluviômetro-ΔV 0 (ΔV do ato 0 hm³)
- sombra (cj_lat, c/ laterais): ~5.5 m (cj 0 mm · Δcj_lat−cj_v07 = -0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.7 m → Alerta (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|

## Chuva-jusante fundida DO ATO — soma horária desde o vale (8 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Salete | 1.6 |
| Rio do Sul | 1.0 |
| Rio do Oeste | 0.4 |
| Agronomica | 0.2 |
| Trombudo Central | 0.1 |
| Ituporanga | 0.0 |
| Taio | 0.0 |
| Aurora | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 1.0, Alfredo Wagner 0.0, Rio do Campo 0.0

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **SDC+offset (DC-RS indisponível, off=-0.16)** · offset medido DC-RS−SDC: **None m** · fallback -0.16 m
- **A) SDC-00013:** baseline 5.63 m · pico v1.0 ~5.6 m (banda 5.2–6.1) → **Alerta**
- **B) DC-RS Dom Tito:** baseline 5.47 m · pico v1.0 ~5.5 m (banda 5.0–6.0) → **Atenção**
- **Δ pico (B − A): -0.10 m** · ⚠ MUDA A CLASSE: Alerta → Atenção
- nível atual: SDC 5.82 m · DC-RS None m

## ⚠ Avisos desta coleta

- barragens(Asthon): <urlopen error [Errno 104] Connection reset by peer>
- DC-RS Ponte Dom Tito indisponível nesta coleta — usando SDC+offset
- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
