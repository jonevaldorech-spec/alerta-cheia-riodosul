# Cheia — Rio do Sul (SC) — 2026-10-16 21:17 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.26 m — **Normal** · tendência estável/caindo
- SDC-00013: 4.32 m · DC-RS Dom Tito: 4.26 m · offset medido DC-RS−SDC: -0.06 m
**Chuva 24h máx (drivers):** 84.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.27 m → **Normal** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.009 m/h (anterior 0.024 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: sem dado · Trombudo Central: sem dado · Agrolandia: sem dado · ⚠ sem confirmação de régua-líder
- o v1.0 vira **TETO** (~3.8 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~3.8 m (banda p10–p90 3.4–4.3 m) → **Normal**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.91 m em 15/10 23:09 (DC-RS) · subida até agora 1.35 m
- chuva-jusante do ato: 22.0 mm (ancoras; acumulado rolante ch24h do painel (histórico do ato insuficiente: 6 h, cobertura 27%)) · chuva-acima 14.3 mm
- cj efetiva 27 mm = cj 22 + trânsito-acima 4 (fração de comportas aberta 0.74) + pluviômetro-ΔV 1 (ΔV do ato 1.4 hm³)
- sombra (cj_lat, c/ laterais): ~3.8 m (cj 20 mm · Δcj_lat−cj_v07 = -3.2 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~4.3 m → Normal (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 1.33 → 2.7 | 1.4 | 1.00 | 7A/0F | 7.05 m |  |
| Sul | 0.01 → 0.0 | 0.0 | 0.48 | 4A/1F | 6.0 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch24h do painel (histórico do ato insuficiente: 6 h, cobertura 27%)

| Município | Chuva do ato (mm) |
|---|---|
| Aurora | 56.4 |
| Trombudo Central | 36.5 |
| Rio do Sul | 33.3 |
| Taio | 22.1 |
| Agrolandia | 21.0 |
| Pouso Redondo | 20.8 |
| Laurentino | 19.6 |
| Agronomica | 13.4 |
| Rio do Oeste | 13.0 |
| Salete | 11.4 |
| Ituporanga | 10.5 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 20.6, Rio do Campo 14.6, Alfredo Wagner 7.6

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 2.7 | 7A/0F | 0 | 7.05 m | 16/10 21:15 |
| Barragem Sul Ituporanga | 0.0 | 4A/1F | 0 | 6.0 m | 16/10 21:15 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.06 m** · fallback -0.07 m
- **A) SDC-00013:** baseline 2.98 m · pico v1.0 ~3.9 m (banda 3.4–4.4) → **Normal**
- **B) DC-RS Dom Tito:** baseline 2.91 m · pico v1.0 ~3.8 m (banda 3.4–4.3) → **Normal**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.32 m · DC-RS 4.26 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.88 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
