---
name: pattern-analyzer
version: "1.0.0"
description: >
  Rejection pattern analysis powered by career-ops.
  Analyzes application outcomes by archetype, ATS vendor, score threshold, remote policy, and tech stack gaps.
  Use when user wants to understand why applications fail or what's working.
triggers:
  - command: PATTERNS
    description: "Run full rejection pattern analysis"
    options:
      - "--quick" : Light check — pending outcomes only
      - "--min-threshold N" : Require min N entries per pattern (default 3)
  - command: LEARN [company] --deep
    description: "Old LEARN command now also triggers pattern analysis"
---

# PATTERN ANALYZER SKILL — career-ops Pattern Adapter

## Location
Analyzer script: `lib/career-ops/analyze-patterns.mjs`
Tracker: `data/pipeline/PIPELINE.md` (parsed via tracker-parse)
Reports: `lib/career-ops/reports/`

## Commands

### PATTERNS — Full Analysis

```bash
node lib/career-ops/analyze-patterns.mjs          # JSON to stdout
node lib/career-ops/analyze-patterns.mjs --summary # human-readable table
```

**Output dimensions:**
| Key | What It Tells You |
|-----|-------------------|
| `metadata` | Total entries, date range, outcome counts |
| `funnel` | Count per stage (evaluated, applied, interview, offer) |
| `scoreComparison` | Avg/min/max score per outcome group |
| `archetypeBreakdown` | Per-archetype conversion rate (which pipe framing wins?) |
| `blockerAnalysis` | Most frequent blockers (geo, stack, seniority) |
| `vendorAnalysis` | ATS vendor conversion rate (Greenhouse vs Lever vs Workday) |
| `remotePolicy` | Remote vs hybrid vs onsite conversion |
| `scoreThreshold` | Data-driven minimum score for applying |
| `recommendations` | Top 5 actionable items |

### Vendor Analysis — Key Insight

Shows which ATS platforms advance you vs block you. If Greenhouse advances at 30% and Workday at 0% across 10+ applications — route Workday companies through referrals instead.

### Integration with LEARN

When `LEARN [company] --deep` runs:
1. Record outcome in `data/learned/[company].md` (existing)
2. Run `node lib/career-ops/analyze-patterns.mjs --summary`
3. Append findings to `reports/pattern-analysis-YYYY-MM-DD.md`
4. Update `data/learned/pipes.md` with new archetype/ATS data
