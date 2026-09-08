# Cheia — Rio do Sul (SC) — 2026-09-08 17:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.51 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 4.7 m · DC-RS Dom Tito: 4.51 m · offset medido DC-RS−SDC: -0.19 m
**Chuva 24h máx (drivers):** 0.2 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.53 m → **ATENÇÃO** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.068 m/h (anterior -0.016 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: subindo · Agrolandia: virou
- o v1.0 vira **TETO** (~3.5 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~3.5 m (banda p10–p90 3.0–4.0 m) → **Normal**
**Classe que dispara o alerta/e-mail: ATENÇÃO**
- baseline = VALE do ato: 3.45 m em 07/09 23:07 (DC-RS) · subida até agora 1.06 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -73% das ancoras); soma horária desde o vale (19 h, cobertura 100%)) · chuva-acima 0.0 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~3.5 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~3.9 m → Normal (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 10.69 → 2.19 | 0.0 | 1.00 | 7A/0F | 7.54 m |  |
| Sul | 16.6 → 6.66 | 0.0 | 1.00 | 5A/0F | 15.0 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (19 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.2 |
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

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 0.1, Alfredo Wagner 0.0, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 2.19 | 7A/0F | 0 | 7.54 m |
| Barragem Sul Ituporanga | 6.66 | 5A/0F | 0 | 15.0 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.19 m** · fallback -0.15 m
- **A) SDC-00013:** baseline 3.6 m · pico v1.0 ~3.6 m (banda 3.1–4.1) → **Normal**
- **B) DC-RS Dom Tito:** baseline 3.45 m · pico v1.0 ~3.5 m (banda 3.0–4.0) → **Normal**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 4.7 m · DC-RS 4.51 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.92 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
