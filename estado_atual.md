# Cheia — Rio do Sul (SC) — 2026-09-02 20:30 (local −03)

**Rio do Sul (DC-RS (Asthon Ponte Dom Tito)):** 5.44 m — **ATENÇÃO** · tendência estável/caindo
- SDC-00013: 5.59 m · DC-RS Dom Tito: 5.44 m · offset medido DC-RS−SDC: -0.15 m
**Chuva 24h máx (drivers):** 0.3 mm
**EVENTO ATIVO:** 🔴 SIM

**Pico estimado (FINO — c/ retenção real das barragens):** ~5.9 m (banda 5.4–6.4 m) → **Alerta**
**Guarda (CONSERVADOR — sem crédito de retenção):** ~5.9 m (banda 5.4–6.4 m) → **Alerta**
**Classe que dispara o alerta/e-mail: Alerta** — usando o CONSERVADOR (há fallback de barragem; o fino não rebaixa alerta enquanto a retenção não é comprovada).
- baseline (mín 48h): 5.44 m · chuva-jusante efetiva: 8 mm · antecedência ~6–12 h
- sombra (cj_lat, c/ laterais): ~5.9 m (cj 7 mm · Δcj_lat−cj_v07 = -0.7 mm, n_laterais=4)

### Crédito de retenção por barragem (peak-shaving)

| Barragem | Ocupação | Montante ini→fim (m) | Taxa (m/h) | Retido (hm³) | Corte (m³/s) | Crédito |
|---|---|---|---|---|---|---|
| Oeste | 51.27% (curva 51.9%) | 17.37→17.45 | 0.01 | 0.59 | 21.0 | ✅ aplicado |
| Sul | 60.89% (curva 60.7%) | 26.47→26.47 | 0.0 | 0.0 | 0.0 | ⚠ 0 — não está enchendo (taxa ≤ 0) — sem crédito |
- termo de barragem (fino): Oeste reteve 0.6 hm³ na janela (~21 m³/s; ocup.~51%) | Sul reteve 0.0 hm³ na janela (~0 m³/s; ocup.~61%) | corte 21 m³/s ÷ DQDH 700 -0.03 m -> ajuste líquido -0.03 m

## Chuva-jusante fundida (48h) — entra no cj oficial

| Município | Chuva 48h (mm) |
|---|---|
| Rio do Sul | 8.4 |
| Taio | 6.6 |
| Aurora | 6.4 |
| Pouso Redondo | 5.9 |
| Trombudo Central | 5.8 |
| Salete | 5.4 |
| Agrolandia | 5.3 |
| Ituporanga | 5.2 |
| Laurentino | 4.6 |
| Rio do Oeste | 4.4 |
| Agronomica | 4.4 |

_Chuva-acima (contexto de barragem, fora do cj):_ Rio do Campo 7.0, Taio_montante 6.0, Alfredo Wagner 3.8

## Barragens (Asthon)

| Barragem | % uso | Comportas | Vertido | Montante |
|---|---|---|---|---|
| Barragem Oeste Taió | 51.27 | 2A/5F | 0 | 17.45 m |
| Barragem Sul Ituporanga | 60.89 | 2A/3F | 0 | 26.47 m |

## Referência de nível — DC-RS Dom Tito (troca de datum)

Referência ATIVA: **DC-RS (Asthon Ponte Dom Tito)** · offset medido DC-RS−SDC: **-0.15 m** · fallback -0.18 m
- **A) SDC-00013 (como era):** baseline 5.61 m · pico FINO ~6.0 m (banda 5.5–6.5) → **Alerta**
- **B) DC-RS Dom Tito (como fica):** baseline 5.44 m · pico FINO ~5.9 m (banda 5.4–6.4) → **Alerta**
- **Δ pico (B − A): -0.10 m** · classe inalterada
- nível atual: SDC 5.59 m · DC-RS 5.44 m · Kanitz (checagem, offset→Dom Tito NÃO CALIBRADO): 4.1 m

## ⚠ Avisos desta coleta

- Sensores TRAVADOS (descartados na fusão): 00022 (SDC-SC Rio do Oeste)
