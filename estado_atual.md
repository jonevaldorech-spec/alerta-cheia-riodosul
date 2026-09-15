# Cheia — Rio do Sul (SC) — 2026-09-15 02:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.08 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 5.23 m · DC-RS Dom Tito: 5.08 m · offset medido DC-RS−SDC: -0.15 m
**Chuva 24h máx (drivers):** 0.8 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~5.08 m → **ATENÇÃO** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual 0.0 m/h (anterior 0.003 m/h) · chuva-driver 2h 0.0 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: subindo
- o v1.0 vira **TETO** (~5.1 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~5.1 m (banda p10–p90 4.6–5.6 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ATENÇÃO**
- baseline = VALE do ato: 5.06 m em 14/09 18:27 (DC-RS) · subida até agora 0.02 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -66% das ancoras); soma horária desde o vale (9 h, cobertura 100%)) · chuva-acima 0.4 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 0.99) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~5.1 m (cj 0 mm · Δcj_lat−cj_v07 = 0.1 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~5.3 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 63.99 → 60.4 | 0.0 | 0.98 | 7A/0F | 18.65 m |  |
| Sul | 15.52 → 15.52 | 0.0 | 1.00 | 5A/0F | 18.2 m |  |

## Chuva-jusante fundida DO ATO — soma horária desde o vale (9 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Ituporanga | 0.4 |
| Aurora | 0.1 |
| Rio do Sul | 0.0 |
| Taio | 0.0 |
| Salete | 0.0 |
| Rio do Oeste | 0.0 |
| Laurentino | 0.0 |
| Pouso Redondo | 0.0 |
| Agrolandia | 0.0 |
| Trombudo Central | 0.0 |
| Agronomica | 0.0 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 1.2, Alfredo Wagner 0.1, Taio_montante 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 60.4 | 7A/0F | 0 | 18.65 m | 15/09 02:22 |
| Barragem Sul Ituporanga | 15.52 | 5A/0F | 0 | 18.2 m | 15/09 02:22 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.15 m** · fallback -0.16 m
- **A) SDC-00013:** baseline 5.22 m · pico v1.0 ~5.2 m (banda 4.7–5.7) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 5.06 m · pico v1.0 ~5.1 m (banda 4.6–5.6) → **Atenção**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 5.23 m · DC-RS 5.08 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 5.32 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
