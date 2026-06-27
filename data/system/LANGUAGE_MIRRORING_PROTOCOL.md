# LANGUAGE MIRRORING PROTOCOL

## Purpose
Extract JD vocabulary, map to Master Corpus facts, and weave into resume + cover letter so the ATS sees 2-4% keyword density AND a human reads a coherent narrative — all without fabrication.

## Core Principle
**100% mirror, zero lies.** Every claim in every output must trace back to `01_MASTER_CORPUS.md` (JOBS-OS). Masquerade = reframing real facts. Fabrication = inventing new ones. Only the former is permitted.

## Protocol Steps

### Step 1 — JD Verb Extraction

Extract ALL verbs and nouns from the JD. Categorize into:

| Category | Examples | Purpose |
|----------|----------|---------|
| **Action verbs** | led, managed, built, scaled, transformed, optimized, delivered | Use in resume bullets |
| **Domain nouns** | operations, strategy, transformation, technology, change management, P&L | Use in summary + experience |
| **Soft skills** | stakeholder management, cross-functional, communication, leadership | Use in summary + cover letter |
| **Technical nouns** | ERP, CRM, data analysis, KPIs, OKRs, reporting, compliance | Use in technical skills section |
| **Cultural words** | agile, fast-paced, collaborative, ownership, growth | Use in cover letter tone |

### Step 2 — Master Corpus Cross-Reference

For each extracted word/phrase, check if Master Corpus contains a claim matching it.

| JD Phrase | Master Corpus Fact | Match? | Reframe? |
|-----------|-------------------|--------|----------|
| "led strategic transformation" | Module E: Led OKR/strategy implementation across 12 departments | ✅ Direct | No reframe needed |
| "managed P&L of $X" | Module F: Managed $5M+ budget, 20% under cost | ✅ Direct | Recast scale |
| "built technology systems" | Module H: Designed EHR, billing, scheduling, RCM systems | ✅ Direct | No reframe needed |
| "M&A integration" | Module C: Scouted 50+ targets across 5 states, led integration | ✅ Direct | No reframe needed |

If a JD phrase has NO match in Master Corpus → ⚠️ FLAG. Do not fabricate. Either:
- Find an adjacent truth that maps semantically
- Omit the claim entirely
- Return to user with: "JD requires [X], Master Corpus has no match. Use adjacent truth [Y] or omit?"

### Step 3 — Density Targeting

Target **2-4% keyword density** in the resume (based on JD-specific keywords). Higher = keyword stuffing (penalized by humans + some ATS). Lower = missed parsing.

| Section | Target Density | Method |
|---------|---------------|--------|
| Professional Summary | 4-5% | Highest concentration — headline + first 2 lines |
| Experience bullets | 2-3% | Weave naturally into existing achievements |
| Skills section | 5-8% | Pure keyword list (this is where density lives) |
| Cover letter | 1-2% | Natural language, one or two JD phrases |

### Step 4 — Bullet Alchemy Formula

```
Before: "Managed operations for a clinic network delivering $4M annual revenue"
After:  "[JD Verb] [achievement from Master Corpus] resulting in [metric]"

Example:
"Led strategic transformation of operations across 5-site clinic network, implementing ERP/EMR systems that drove $4M annual revenue and 62% faster implementations."
```

**Rules:**
- Lead every bullet with an action verb from the JD
- Include at least one metric per bullet (from Master Corpus)
- Tag each claim with the Master Corpus line number during SHOOT generation
- Max 6 bullets per role, 4 bullets for non-core roles

### Step 5 — Provenance Verification

Before output, run:

```
For each claim in resume/cover letter:
  → Check Master Corpus for underlying fact
  → If found: note line number → PASS
  → If NOT found: ⚠️ FLAG
  → If masquerade: verify underlying fact has source line number
```

### Step 6 — ATS-Specific Delivery

Per ATS platform (from ATS_ESOTERICA.md):

| Platform | Delivery Instructions |
|----------|----------------------|
| Greenhouse | Exact JD keyword matching (synonyms score lower) |
| Workday | Simple PDF, no tables/columns/graphics |
| SAP SuccessFactors | No headers/footers with personal info |
| Lever | Simple formatting, referral source preferred |
| UltiPro | Cover letter matters more — write a good one |

## Language Registry Template

For every SHOOT, generate a language registry before writing:

```
## [COMPANY] — LANGUAGE REGISTRY

### JD Verbs Extracted
- word1 (count: N)
- word2 (count: N)
- ...

### Master Corpus Matches
| JD Phrase | Corpus Fact | Line # | Verdict |
|-----------|-------------|--------|---------|

### Density Plan
- Summary: [N]% target — [phrases to include]
- Skills: [N]% target — [keywords to list]
- Experience: [N]% target — [bullets to rewrite]

### Cultural Tone
[JD tone analysis — formal? innovative? collaborative?]
[Company values mentioned in JD]
[Perception mode to use: Authentic/Hybrid/Machiavellian]
```

## Zero-Fabrication Checklist
- [ ] Every claim cross-referenced to Master Corpus
- [ ] Masquerade reframes real facts (title adjustments, scope framing)
- [ ] No invented metrics, timelines, or outcomes
- [ ] Immigration language absent from all written materials
- [ ] JD keyword density 2-4% (not stuffed, not missing)
- [ ] Cultural tone matches company's internal language
- [ ] ATS format rules applied per platform
