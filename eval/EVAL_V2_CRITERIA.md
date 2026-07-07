# EVAL V2 — 10-Dimension Scoring Criteria
## Enhanced from OPS_EVAL_CRITERIA.md + career-ops process-quality.mjs

## Scoring System
Each dimension scored 1-10 (10 = perfect). Total = sum of all 10 = max 100.
PASS ≥ 70, WARN 50-69, FAIL < 50.

## Dimensions

### D1: Role Fit (Weight: 2x)
**What it measures:** How well Aman's actual experience matches the JD requirements.
- 9-10: Direct match — same level, same function, same industry
- 7-8: Strong match — same function, different industry or slightly different level
- 5-6: Moderate match — adjacent function or significant level difference
- 3-4: Weak match — different domain, some transferable skills
- 1-2: Stretch — major pivot required

### D2: CV Match (Weight: 1x)
**What it measures:** How well the resume communicates fit for THIS specific role.
- 9-10: Keywords mirror JD, bullets address every requirement, narrative flows
- 7-8: Most keywords present, 80%+ requirements addressed
- 5-6: Some keywords, core requirements addressed
- 3-4: Generic resume, few JD-specific adjustments
- 1-2: Template resume, no customization visible

### D3: Level Strategy (Weight: 1x)
**What it measures:** Whether the target level is realistic and strategic.
- 9-10: Perfect level — credible based on experience, competitive comp
- 7-8: Slight stretch or slight undershoot — still reasonable
- 5-6: Significant stretch or undershoot — needs justification
- 3-4: Wrong level — likely rejected as over/underqualified
- 1-2: Incoherent — title and responsibilities don't match

### D4: Compensation Research (Weight: 1x)
**What it measures:** Quality of salary benchmarking and negotiation position.
- 9-10: Glassdoor + Levels + Blind data, BATNA defined, anchoring strategy ready
- 7-8: Glassdoor data, ballpark range known
- 5-6: Rough range, no anchoring strategy
- 3-4: No salary research
- 1-2: Guessing

### D5: Personalization (Weight: 1x)
**What it measures:** Degree of company-specific tailoring in application.
- 9-10: Cover letter references specific initiatives, language registry woven in, custom answers
- 7-8: Company-name-level customization, some JD language reflected
- 5-6: Generic cover letter with company name swapped
- 3-4: No cover letter, no customization
- 1-2: Spray-and-pray template

### D6: Interview Prep (Weight: 1.5x)
**What it measures:** Readiness for the specific company's interview process.
- 9-10: Process stages known, sample questions prepped, STAR stories ready, company research deck done
- 7-8: Process known, 2-3 stories prepped
- 5-6: Process known but no prep
- 3-4: Unknown process, no prep
- 1-2: Flying blind

### D7: Company Trajectory (Weight: 0.5x)
**What it measures:** Whether the company is growing, stable, or declining.
- 9-10: Hypergrowth (30%+ YoY), recent funding, expanding headcount
- 7-8: Stable growth (10-30% YoY), healthy margins
- 5-6: Mature/slow growth, stable
- 3-4: Declining, recent layoffs, shrinking headcount
- 1-2: Distressed, known to be in trouble

### D8: Team Quality (Weight: 0.5x)
**What it measures:** Quality of the team Aman would join (Glassdoor reviews, LinkedIn profiles, team size).
- 9-10: Well-rated team, experienced peers, good Glassdoor reviews
- 7-8: Solid team, average reviews
- 5-6: Unknown team, no signal
- 3-4: Poor reviews, high turnover in this team
- 1-2: Toxic reputation

### D9: Location & Practicality (Weight: 0.5x)
**What it measures:** Whether the location/remote setup is feasible.
- 9-10: Remote Canada or Vancouver office, ideal commute
- 7-8: Vancouver area, reasonable commute
- 5-6: BC but outside GVA
- 3-4: Canada but outside BC
- 1-2: US or international (requires visa)

### D10: Ghost/Scam Detection (Weight: 0.5x)
**What it measures:** Whether the posting is legitimate.
- 10: Verified live, recent posting, no red flags
- 8: Seems legitimate, recent posting
- 6: No signal either way
- 4: Stale posting (>60 days) or suspicious
- 2: Likely ghost job or scam
- 1: Confirmed ghost/scam

## Scoring Calculation

```
Raw Score = Σ(D1×2 + D2×1 + D3×1 + D4×1 + D5×1 + D6×1.5 + D7×0.5 + D8×0.5 + D9×0.5 + D10×0.5)
Max Score = 10×(2+1+1+1+1+1.5+0.5+0.5+0.5+0.5) = 10×9.5 = 95

Normalized Score = (Raw Score / 95) × 100

PASS  ≥ 70
WARN  50-69
FAIL  < 50
```

## Quality Dashboard Output

```
╔══════════════════════════════════════════════════════════════════╗
║  EVAL V2 — [Company] [Role]                                    ║
╠══════════════════════════════════════════════════════════════════╣
║  D1 Role Fit:          8/10 (×2) = 16     ■■■■■■■■□□            ║
║  D2 CV Match:          7/10 (×1) = 7      ■■■■■■■□□□            ║
║  D3 Level Strategy:    7/10 (×1) = 7      ■■■■■■■□□□            ║
║  D4 Comp Research:     8/10 (×1) = 8      ■■■■■■■■□□            ║
║  D5 Personalization:   8/10 (×1) = 8      ■■■■■■■■□□            ║
║  D6 Interview Prep:    6/10 (×1.5) = 9    ■■■■■■□□□□            ║
║  D7 Co Trajectory:     7/10 (×0.5) = 3.5  ■■■■■■■□□□            ║
║  D8 Team Quality:      6/10 (×0.5) = 3    ■■■■■■□□□□            ║
║  D9 Location:          9/10 (×0.5) = 4.5  ■■■■■■■■■□            ║
║  D10 Ghost Check:      8/10 (×0.5) = 4    ■■■■■■■■□□            ║
╠══════════════════════════════════════════════════════════════════╣
║  RAW SCORE: 70 / 95 × 100 = 73.7 → PASS ✅                      ║
║  STRONGEST: Role Fit (8), Location (9)                          ║
║  WEAKEST: Interview Prep (6), Team Quality (6)                  ║
║  RECOMMENDATION: Proceed with SHOOT → prep interview stage      ║
╚══════════════════════════════════════════════════════════════════╝
```
