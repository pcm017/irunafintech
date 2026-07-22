---
layout: post
title: 'Source: Tech & AI Digest — 2026-06-25'
date: 2026-06-25 08:00:00 +0530
categories:
- newsletter
tags:
- ai
- tech
- llm
- india-semiconductor
- turiyam
- inference-chip
- nvidia
- tsmc
- asml
- imec
- chip-manufacturing
- q1-2026-chip-sales
- ai-capex-skepticism
- china-tech
---

# Source: Tech & AI Digest — 2026-06-25

**TL;DR**
- Turiyam: India's first inference chip company (Bengaluru, Dec 2024) builds full-stack inference silicon without Nvidia CUDA dependency; charges per compute not per token; addresses exploding enterprise AI bills; TCS-Anthropic export control timing created the window for this thesis
- Global semiconductor sales Q1 2026: $298.5B (+25% QoQ) — industry on track for $1T full-year 2026; paradoxical against AI spending skepticism selloff
- TSMC+ASML+Imec demonstrate 300mm 2D transistor integration route — next-generation transistor manufacturing beyond silicon at advanced nodes
- TSMC CoPoS validation underway (first demo tools entering validation) — next-gen AI GPU packaging capacity ramp timeline
- Noah Smith on China's tech comeback; AI spending skepticism drove S&P -1.44% June 23 but semiconductor demand data remains robust

---

## Key Data / Quotes

### Turiyam — India's First Inference Chip Company (Full Profile)

**Company:** Turiyam, Bengaluru
**Founded:** December 2024
**Founders:** Sanchayan Sinha (CEO), Parag Jain, Praveen Jain
**Thesis:** Full-stack inference silicon without Nvidia CUDA dependency

**The problem they're solving:** Enterprise AI costs are exploding while token prices fall. Token prices have dropped 35% over two years, but enterprise AI bills have risen 6× — reaching $7M annually for some large customers. The disconnect: volume (more inference, not higher per-token prices). Turiyam's model: charges **per compute** rather than per token, positioning as cost-neutral for high-volume inference users.

**Architecture:** Full stack — chip architecture + compiler + runtime + inference serving layer. No NVIDIA CUDA ecosystem dependency. Designed for enterprises running high-volume inference at scale.

**Key context:** TCS signed an exclusive partnership with Anthropic one day before the US export order took effect, cutting off access to specific Anthropic models. This created a window for inference infrastructure built around non-US model providers — precisely what Turiyam is positioned to address.

**Status:** Operating in stealth. Engaged with at least one major Indian IT services firm. No funding disclosed publicly (as of June 24 publication date).

*Significance: India has strong semiconductor design talent (40%+ of global chip design engineers are Indian) but zero domestic silicon for AI inference. Turiyam is the first company attempting to change this — and is doing so at a moment when US export controls are creating structural demand for non-US-dependent AI infrastructure.*

### Global Semiconductor Sales Q1 2026
- **$298.5 billion** — Q1 2026 global chip sales
- **+25% QoQ** growth vs. Q4 2025
- **$1 trillion** projected for full-year 2026 (first ever if achieved)

*Paradox: The June 23 AI spending skepticism selloff (-1.44% S&P, -2.21% Nasdaq) happened despite this strong demand data. The market is debating AI equity valuations (multiple compression) while the underlying semiconductor demand remains robust.*

### TSMC + ASML + Imec: 2D Transistor 300mm Route
**TSMC**, **ASML**, and **Imec** (Belgium-based semiconductor R&D) have demonstrated a **300mm integration route for 2D-material n-type and p-type field-effect transistors** — a milestone toward manufacturing next-generation transistors beyond silicon at sub-2nm nodes.

**Why this matters:**
- Conventional silicon transistors are approaching physical scaling limits at the 2nm node and below
- 2D materials (molybdenum disulfide, tungsten diselenide) maintain transistor properties at near-atomic thicknesses where silicon fails
- 300mm = current standard wafer size for production fabs — demonstrating 2D integration on 300mm is the step between lab demonstration and manufacturing feasibility
- ASML's role: High-NA EUV will be required for the lithography steps at sub-2nm with 2D materials
- *Timeline for production: 2030-2032 likely for high-volume manufacturing*

### NVIDIA + TSMC: cuLitho + H200 in Fabs
**TSMC** deploying **NVIDIA cuLitho** (GPU-accelerated computational lithography) on **NVIDIA H200 GPUs** at TSMC fabs:
- 20-50% improvement in cost effectiveness or cycle time vs. CPU-based approaches
- TSMC CoPoS rollout: first CoPoS demo tools entering validation — CoPoS replaces round silicon wafers with larger rectangular glass panels for AI GPU/HPC packaging

### AI Spending Skepticism vs. Semiconductor Demand
S&P -1.44%, Nasdaq -2.21% on June 23 — "Wall Street gets an AI wake-up call" (Bloomberg). The selloff reflects investor doubt about whether hyperscaler AI data center capex is generating sufficient ROI to justify AI equity multiples.

But Q1 2026 chip sales at $298.5B (+25% QoQ) suggest end-demand for AI compute is structurally strong. The tension: market pricing (multiple compression) vs. physical demand (still accelerating).

### Noah Smith on China's Tech Comeback
Noah Smith (Noahpinion, June 24) — "China's Tech Comeback." Likely covers: DeepSeek's global impact, China's domestic AI model development, and semiconductor self-sufficiency push. Context: PBoC Governor Pan Gongsheng spoke on China's financial modernisation at Lujiazui Forum (June 17) — aligned timing.

---

## Signals

- **Turiyam = India's first AI silicon play — and the timing is right:** The TCS-Anthropic US export control timing (partnership signed one day before the export order) illustrates the geopolitical exposure of India's AI infrastructure dependency. Turiyam's full-stack, no-CUDA approach directly addresses this. For the wiki: Turiyam deserves its own entity page in `wiki/companies/` or `wiki/ai-tech/` as India's first inference chip company. Key metrics to track: funding round, first customer deployment, benchmark results vs. NVIDIA inference performance
- **$1T chip market in 2026 — but the gains are concentrated:** $298.5B Q1 driven primarily by AI/HPC demand (NVIDIA H100/H200/B200; SK Hynix HBM; TSMC CoWoS). CXMT's HBM ambitions (see June 24 digest) are aimed directly at this segment. India has no significant share of this $1T market today — Turiyam, Tata Electronics (assembly), and ISM fabs are all pre-revenue in this category
- **TSMC+ASML+Imec 2D transistor = 5-10 year horizon signal:** This is not a near-term trading catalyst but a fundamental signal about where semiconductor roadmaps go post-silicon. For India's ISM strategy (which is focused on mature nodes and ATMP): by the time India's Sanand fab (Tata Electronics) or Dholera fab (Tata Electronics) reaches advanced nodes, 2D transistors may be the relevant technology node. India's ISM planning needs a 2030-2035 technology roadmap view, not just a 2026-2028 capacity view
- **AI spending skepticism paradox:** The June 23 selloff + strong Q1 chip data creates a useful analytical distinction. AI equity multiples are compressing (multiple de-rating on ROI uncertainty) while AI infrastructure demand remains robust (real compute sales still growing 25% QoQ). India's IT sector and tech investors need to distinguish: (1) frontier AI model company valuations (where multiple pressure is happening) vs. (2) AI infrastructure/chip demand (where physical demand is intact)

---

## Cross-References
- *overview* — Updated: AI & Tech section
- *india ai* — Turiyam: India's first inference chip company
- *tcs* — TCS-Anthropic export control timing creates Turiyam market window

---

## Raw File
`raw/newsletters/2026-06-25-tech-ai-digest.md`
