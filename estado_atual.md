# Cheia — Rio do Sul (SC) — 2026-10-16 06:14 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.33 m — **Normal** · tendência subindo
- SDC-00013: 4.4 m · DC-RS Dom Tito: 4.33 m · offset medido DC-RS−SDC: -0.07 m
**Chuva 24h máx (drivers):** 85.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.35 m → **Normal** · crista em ~1 h
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.076 m/h (anterior 0.192 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: sem dado · Trombudo Central: sem dado · Agrolandia: sem dado · ⚠ sem confirmação de régua-líder
- o v1.0 vira **TETO** (~3.8 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~3.8 m (banda p10–p90 3.3–4.3 m) → **Normal**
**Classe que dispara o alerta/e-mail: Normal**
- baseline = VALE do ato: 2.91 m em 15/10 23:09 (DC-RS) · subida até agora 1.42 m
- chuva-jusante do ato: 22.4 mm (ancoras; acumulado rolante ch24h do painel (histórico do ato insuficiente: 2 h, cobertura 28%)) · chuva-acima 14.5 mm
- cj efetiva 27 mm = cj 22 + trânsito-acima 4 (fração de comportas aberta 0.70) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~3.8 m (cj 21 mm · Δcj_lat−cj_v07 = -2.7 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~4.3 m → Normal (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 1.33 → 0.07 | 0.0 | 1.00 | 7A/0F | 3.45 m |  |
| Sul | 0.01 → 0.01 | 0.0 | 0.40 | 2A/3F | 7.0 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch24h do painel (histórico do ato insuficiente: 2 h, cobertura 28%)

| Município | Chuva do ato (mm) |
|---|---|
| Aurora | 57.1 |
| Trombudo Central | 37.8 |
| Rio do Sul | 33.5 |
| Taio | 22.6 |
| Agrolandia | 22.2 |
| Pouso Redondo | 20.0 |
| Laurentino | 19.6 |
| Agronomica | 13.6 |
| Rio do Oeste | 13.0 |
| Salete | 12.4 |
| Ituporanga | 11.1 |

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 21.4, Rio do Campo 14.5, Alfredo Wagner 7.6

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 0.07 | 7A/0F | 0 | 3.45 m | 16/10 06:13 |
| Barragem Sul Ituporanga | 0.01 | 2A/3F | 0 | 7.0 m | 16/10 06:13 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.07 m** · fallback -0.12 m
- **A) SDC-00013:** baseline 3.03 m · pico v1.0 ~3.9 m (banda 3.4–4.4) → **Normal**
- **B) DC-RS Dom Tito:** baseline 2.91 m · pico v1.0 ~3.8 m (banda 3.3–4.3) → **Normal**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.4 m · DC-RS 4.33 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.68 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
