# THE GATE — Pre-SHOOT Fitness Assessment

## Purpose
A standardized binary gate that runs BEFORE any SHOOT package is generated. Prevents wasting resources on jobs that fail fundamental fit criteria.

## The Gate Questions (10-Question Binary)

| # | Question | Pass Condition | Auto-Fail |
|---|----------|---------------|-----------|
| 1 | **Salary floor?** | Min $80K, target ≥ $120K | < $80K → STOP |
| 2 | **Location fit?** | Vancouver/Remote Canada | On-site elsewhere → STOP |
| 3 | **TEER 0/1?** | Yes | TEER 2/3 → STOP (no PR qualification) |
| 4 | **Credit check?** | No | Yes → STOP silently |
| 5 | **Heavy quant/Excel?** | No | Financial modeling, VBA, FP&A, data science → STOP |
| 6 | **Domain pivot?** | Operations/Strategy/GM/Program Mgt only | TPM, SWE, Security, AI/ML, Quant → STOP |
| 7 | **Freshness?** | Posted ≤ 24h from FETCH | > 24h → STOP (fetch fresh) |
| 8 | **Fit score ≥ 65?** | Yes, from HONEST FIT SCORECARD | < 65 → STOP (unless user override) |
| 9 | **JD readability?** | Role & scope are clear | Confusing/incoherent JD → STOP |
| 10 | **No immigration on written materials** | Resume/cover/LinkedIn have zero immigration language | Contains visa/PR/PGWP/work permit → STOP |

## HONEST FIT SCORECARD (0-100)

### Scoring Rubric

| Dimension | Weight | 0-40 (Weak) | 41-60 (Moderate) | 61-80 (Strong) | 81-100 (Elite) |
|-----------|--------|-------------|------------------|----------------|-----------------|
| Narrative alignment | 25% | Story doesn't fit | Tangential | Clear bridge | "Already one of them" |
| JD verb match | 20% | < 30% overlap | 30-50% | 50-70% | > 70% |
| Salary feasibility | 15% | Below floor | At floor | Mid-range | Top-half achievable |
| ATS feasibility | 15% | Unknown ATS | Difficult ATS | Standard ATS | Known compatible |
| Competition | 10% | Extreme | High | Moderate | Low (niche fit) |
| User interest | 15% | Low | Medium | High | "This is the one" |

### Scoring Formula
```
SCORE = (Narrative × 0.25) + (VerbMatch × 0.20) + (Salary × 0.15) + (ATS × 0.15) + (Competition × 0.10) + (Interest × 0.15)
```

### Thresholds
| Score | Verdict |
|-------|---------|
| ≥ 85 | Tier 1 (Trust) — auto-approve after quick summary |
| 65-84 | Tier 2 (Normal) — full 16-section SHOOT review |
| 50-64 | Tier 3 (Strategic) — strategy discussion required |
| < 50 | HOLD unless user explicitly overrides |

## Override Mechanism
User can override any gate result with: `FORCE [company] [reason]`

Overrides are logged to `data/learned/[company].md` for audit trail.

## Auto-Fail (No Override)
| Condition | Rationale |
|-----------|-----------|
| Credit check required | Non-negotiable per personal data policy |
| Heavy quant/Excel role | Non-negotiable per personal data policy |
| Domain pivot to forbidden realm | Hard rule — immutable |
| Immigration language in written materials | Hard rule — handle at interview only |
