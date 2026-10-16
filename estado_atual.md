# Cheia — Rio do Sul (SC) — 2026-10-16 15:17 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.25 m — **Normal** · tendência estável/caindo
- SDC-00013: 4.31 m · DC-RS Dom Tito: 4.25 m · offset medido DC-RS−SDC: -0.06 m
**Chuva 24h máx (drivers):** 85.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.26 m → **Normal** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.028 m/h (anterior -0.014 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: sem dado · Trombudo Central: sem dado · Agrolandia: sem dado · ⚠ sem confirmação de régua-líder
- o v1.0 vira **TETO** (~3.8 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~3.8 m (banda p10–p90 3.3–4.3 m) → **Normal**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.91 m em 15/10 23:09 (DC-RS) · subida até agora 1.34 m
- chuva-jusante do ato: 22.2 mm (ancoras; acumulado rolante ch24h do painel (histórico do ato insuficiente: 4 h, cobertura 25%)) · chuva-acima 14.8 mm
- cj efetiva 27 mm = cj 22 + trânsito-acima 4 (fração de comportas aberta 0.70) + pluviômetro-ΔV 0 (ΔV do ato 0.6 hm³)
- sombra (cj_lat, c/ laterais): ~3.8 m (cj 21 mm · Δcj_lat−cj_v07 = -3.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~4.3 m → Normal (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 1.33 → 1.76 | 0.4 | 1.00 | 7A/0F | 6.75 m |  |
| Sul | 0.01 → 0.18 | 0.2 | 0.40 | 3A/2F | 8.3 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch24h do painel (histórico do ato insuficiente: 4 h, cobertura 25%)

| Município | Chuva do ato (mm) |
|---|---|
| Aurora | 57.1 |
| Trombudo Central | 38.0 |
| Rio do Sul | 33.3 |
| Taio | 22.6 |
| Agrolandia | 21.6 |
| Pouso Redondo | 21.0 |
| Laurentino | 19.6 |
| Agronomica | 13.6 |
| Rio do Oeste | 13.0 |
| Salete | 12.4 |
| Ituporanga | 10.7 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 21.2, Rio do Campo 15.7, Alfredo Wagner 7.6

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 1.76 | 7A/0F | 0 | 6.75 m | 16/10 15:14 |
| Barragem Sul Ituporanga | 0.18 | 3A/2F | 0 | 8.3 m | 16/10 15:14 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.06 m** · fallback -0.11 m
- **A) SDC-00013:** baseline 3.02 m · pico v1.0 ~3.9 m (banda 3.4–4.4) → **Normal**
- **B) DC-RS Dom Tito:** baseline 2.91 m · pico v1.0 ~3.8 m (banda 3.3–4.3) → **Normal**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.31 m · DC-RS 4.25 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.66 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
