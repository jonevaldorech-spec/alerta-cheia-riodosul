# Cheia — Rio do Sul (SC) — 2026-09-16 07:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 4.59 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 4.74 m · DC-RS Dom Tito: 4.59 m · offset medido DC-RS−SDC: -0.15 m
**Chuva 24h máx (drivers):** 0.5 mm
**EVENTO ATIVO:** 🔴 SIM

**🎯 MODO CRISTA (nowcast — chuva encerrada, réguas-líder viradas):** pico ~4.6 m → **ATENÇÃO** · crista já atingida/passando
- método: projeção da trajetória (decaimento linear da taxa, validado −0,03/+0,02 nos ev.15/16). Taxa atual -0.076 m/h (anterior -0.064 m/h) · chuva-driver 2h 0.1 mm/h
- réguas-líder: Pouso Redondo: virou · Trombudo Central: virou · Agrolandia: virou
- o v1.0 vira **TETO** (~4.6 m); o número acima é o nowcast e DECIDE o alerta.

**Pico estimado (v1.0 (TETO — modo crista ativo)):** ~4.6 m (banda p10–p90 4.1–5.1 m) → **Atenção**
**Classe que dispara o alerta/e-mail: ATENÇÃO**
- baseline = VALE do ato: 4.59 m em 16/09 07:28 (DC-RS) · subida até agora 0.0 m
- chuva-jusante do ato: 0.0 mm (drivers (divergiu -73% das ancoras); acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)) · chuva-acima 0.1 mm
- cj efetiva 0 mm = cj 0 + trânsito-acima 0 (fração de comportas aberta 1.00) + pluviômetro-ΔV 0 (ΔV do ato 0.0 hm³)
- sombra (cj_lat, c/ laterais): ~4.6 m (cj 0 mm · Δcj_lat−cj_v07 = 0.0 mm, n_laterais=4)
- modelo antigo v0.9 (conservador, sem crédito de retenção, chuva do ato): ~4.9 m → Atenção (só comparação)

### Barragens no ato (desde o vale)

| Barragem | % no vale → agora | ΔV retido (hm³) | Fração aberta (média) | Comportas | Montante | Obs |
|---|---|---|---|---|---|---|
| Oeste | 48.2 → 47.98 | 0.0 | 1.00 | 7A/0F | 17.0 m |  |
| Sul | 1.01 → 0.0 | 0.0 | 1.00 | 5A/0F | 4.0 m |  |

## Chuva-jusante fundida DO ATO — acumulado rolante ch6h do painel (histórico do ato insuficiente: 1 h, cobertura 100%)

| Município | Chuva do ato (mm) |
|---|---|
| Rio do Sul | 0.1 |
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

_Chuva-acima (contexto de barragem, fora do cj):_ Taio_montante 0.2, Alfredo Wagner 0.0, Rio do Campo 0.0

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante | Medida em |
|---|---|---|---|---|---|
| Barragem Oeste Taió | 47.98 | 7A/0F | 0 | 17.0 m | 16/09 07:22 |
| Barragem Sul Ituporanga | 0.0 | 5A/0F | 0 | 4.0 m | 16/09 07:22 |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.15 m** · fallback -0.16 m
- **A) SDC-00013:** baseline 4.75 m · pico v1.0 ~4.8 m (banda 4.3–5.3) → **Atenção**
- **B) DC-RS Dom Tito:** baseline 4.59 m · pico v1.0 ~4.6 m (banda 4.1–5.1) → **Atenção**
- **Δ pico (B − A): -0.20 m** · classe inalterada
- nível atual: SDC 4.74 m · DC-RS 4.59 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 3.61 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
