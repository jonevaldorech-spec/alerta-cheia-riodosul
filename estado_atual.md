# Cheia — Rio do Sul (SC) — 2026-09-02 20:00 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.47 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 5.62 m · DC-RS Dom Tito: 5.47 m · offset medido DC-RS−SDC: -0.15 m
**Chuva 24h máx (drivers):** 0.3 mm
**EVENTO ATIVO:** 🔴 SIM

**Pico estimado (FINO — c/ retenção real das barragens):** ~6.1 m (banda 5.6–6.6 m) → **Alerta**
**Guarda (CONSERVADOR — sem crédito de retenção):** ~6.2 m (banda 5.7–6.7 m) → **Alerta**
**Classe que dispara o alerta/e-mail: Alerta** — usando o CONSERVADOR (há fallback de barragem; o fino não rebaixa alerta enquanto a retenção não é comprovada).
- baseline (mín 48h): 5.47 m · chuva-jusante efetiva: 15 mm · antecedência ~6–12 h
- sombra (cj_lat, c/ laterais): ~6.1 m (cj 13 mm · Δcj_lat−cj_v07 = -1.6 mm, n_laterais=4)

### Crédito de retenção por barragem (peak-shaving)

| Barragem | Ocupação | Montante ini→fim (m) | Taxa (m/h) | Retido (hm³) | Corte (m³/s) | Crédito |
|---|---|---|---|---|---|---|
| Oeste | 51.27% (curva 51.8%) | 17.28→17.44 | 0.02 | 1.18 | 41.0 | ✅ aplicado |
| Sul | 60.89% (curva 60.7%) | 26.47→26.47 | 0.0 | 0.0 | 0.0 | ⚠ 0 — não está enchendo (taxa ≤ 0) — sem crédito |
- termo de barragem (fino): Oeste reteve 1.2 hm³ na janela (~41 m³/s; ocup.~51%) | Sul reteve 0.0 hm³ na janela (~0 m³/s; ocup.~61%) | corte 41 m³/s ÷ DQDH 700 -0.06 m -> ajuste líquido -0.06 m

## Chuva-jusante fundida (48h) — entra no cj oficial

| Município | Chuva 48h (mm) |
|---|---|
| Rio do Sul | 19.6 |
| Taio | 13.7 |
| Aurora | 12.9 |
| Salete | 11.2 |
| Pouso Redondo | 10.9 |
| Laurentino | 10.6 |
| Agronomica | 10.2 |
| Trombudo Central | 9.5 |
| Ituporanga | 9.3 |
| Agrolandia | 9.2 |
| Rio do Oeste | 8.2 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 13.0, Taio_montante 11.6, Alfredo Wagner 6.2

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 51.27 | 2A/5F | 0 | 17.45 m |
| Barragem Sul Ituporanga | 60.89 | 2A/3F | 0 | 26.47 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.15 m** · fallback -0.18 m
- **A) SDC-00013 (como era):** baseline 5.61 m · pico FINO ~6.2 m (banda 5.7–6.8) → **Alerta**
- **B) DC-RS Dom Tito (como fica):** baseline 5.47 m · pico FINO ~6.1 m (banda 5.6–6.6) → **Alerta**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 5.62 m · DC-RS 5.47 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.13 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
