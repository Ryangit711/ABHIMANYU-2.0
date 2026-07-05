---
name: feedback-engine
description: "Triggered by LEARN [company] [outcome], LEARN [company] --deep, PATTERNS, or auto-signal from pipeline-tracker on ❌/💰/📞. Closes the loop: outcome → analysis → system update → pipeline sync. PATTERNS runs career-ops analyze-patterns.mjs for cross-application insights (ATS vendor analysis, archetype performance, score thresholds). Every rejection or offer changes the system permanently. Cross-wired: reads from pipeline, writes to learned files, signals back to pipeline."
---

# FEEDBACK ENGINE — Systemic Learning Loop

## Cross-Skill Wiring

### Inputs (Read From)
| Source | What | When |
|--------|------|------|
| `pipeline-tracker` | company, role, outcome, stage_reached | Auto-signal on ❌/💰/📞 |
| `data/pipeline/PIPELINE.md` | Current pipeline state for this job | On manual LEARN |
| `data/learned/[company].md` | Previous lessons for this company | Always |
| User | Additional context ("they said I lacked X") | On LEARN --deep |
| SHOOT package | Resume text + JD text stored with submission | If available for ATS scoring |

### Outputs (Write To)
| Target | What | When |
|--------|------|------|
| `data/learned/[company].md` | Lesson appended | Every LEARN |
| `data/learned/pipes.md` | Pipe success/fail updated | Every LEARN |
| `data/learned/keywords.md` | Keywords that won/lost | Every LEARN |
| `data/learned/skill_gaps.md` | Flagged skills | If rejection cites skill gap |
| `data/learned/salary.md` | Offer salary data | If 💰 OFFER with amount |
| `data/learned/ats_scores.md` | TF-IDF score + missing keywords for this application | Every LEARN with ATS scoring |
| `pipeline-tracker` | Signal: stage update + ATS score attached | If outcome changes pipeline |

---

## Trigger
- Auto-signal from pipeline-tracker on ❌/💰/📞
- `LEARN [company] [outcome]` — manual
- `LEARN [company] --deep` — full analysis (5-10 min, multi-source)

---

## The Learning Protocol (Run on Every Outcome)

### Step 1: Capture the Outcome
```
READ pipeline for job context: company, role, stage_reached, date submitted
COLLECT from user (if manual) or from pipeline signal:
  Outcome: [offer / callback / rejection / ghosted]
  Stage reached: [applied / screening / interview 1 / interview 2 / final / offer]
  What was said (if anything): [verbatim feedback]
  Offer amount (if 💰): [amount]
```

### Step 2: Analyze Why (Decision Tree)

**If OFFER or CALLBACK:**
```
What worked?
  → Which pipe positioning? (C/T/I/S)
  → Which archetype? (A/B/C)
  → Which keywords resonated?
  → Which STAR story landed?
  → What made this application different?
→ RECORD in data/learned/[company].md
→ UPDATE data/learned/pipes.md: +1 success for this pipe
→ UPDATE data/learned/keywords.md: +1 win for used keywords
→ DOUBLE DOWN on these patterns in future SHOOTs
```

**If REJECTION or GHOSTED:**
```
Why?
  → Skill gap? (what specific skill was missing?) → WRITE to data/learned/skill_gaps.md
  → Experience gap? (industry? level? years?)
  → Positioning mismatch? (wrong pipe? wrong archetype?) → UPDATE data/learned/pipes.md
  → ATS failure? (wrong keywords? format?) → UPDATE data/learned/keywords.md: +1 loss
  → Culture fit? (company DNA misread?)
  → Timing? (hiring freeze? internal candidate?)
→ RECORD in data/learned/[company].md
→ UPDATE data/learned/pipes.md: +1 failure for this pipe
```

### Step 3: Run ATS Scoring (TF-IDF Analysis)

If the SHOOT package included resume text + JD text, run automated ATS scoring:

```
RUN: python3 scripts/ats_scorer.py --resume [resume_text_file] --jd [jd_text_file] --json
  → Score: [0-100]%
  → Missing keywords: [terms in JD not in resume]
  → Matched keywords: [terms in both]

IF score < 50%:
  → Likely ATS keyword mismatch → focus analysis on keyword gaps
  → RECOMMEND: keyword density increase for next SHOOT at similar company
  → UPDATE data/learned/keywords.md: +1 loss for unmatched terms

IF score 50-70%:
  → Moderate match → analyze which keywords carried weight
  → ADD to data/learned/[company].md: ATS score + gap suggestions

IF score > 70%:
  → Good keyword match → failure likely due to positioning/other factors
  → Narrow analysis away from ATS, toward fit/culture/level

STORE score in data/learned/ats_scores.md:
  → Append row: [company] | [role] | [score] | [outcome] | [matched_terms] | [missing_terms]
  → This builds a corpus that predicts: "For this pipe, X score means Y outcome"
```

The ATS score acts as a FOCUSING LENS — it tells you WHERE to look for the problem.

### Step 4: Update the System (The Critical Step)

Based on analysis, make ONE or MORE of these updates:

| Finding | System Change | File Written |
|---------|--------------|--------------|
| Wrong pipe positioning | Update company DNA for this company | `data/learned/[company].md` |
| Wrong archetype | Add note for similar future companies | `data/learned/pipes.md` |
| Missing keywords | Add to learned keywords as "lost" | `data/learned/keywords.md` |
| ATS format failure | Update ATS spec for this platform | `data/learned/[company].md` |
| Skill gap identified | Log for training or reframing | `data/learned/skill_gaps.md` |
| Salary mismatch | Adjust salary data | `data/learned/salary.md` |
| Red flag detected | Add to company anti-patterns | `data/learned/[company].md` |

### Step 5: Write the Lesson

Append to `data/learned/[company].md`:
```
## [YYYY-MM-DD] — [outcome] for [role]

**What happened:** [details]
**Why I think:** [analysis]
**System change made:** [what was updated]
**Lesson for future:** [one-sentence takeaway]
```

### Step 5b — career-ops Pattern Analysis (Enhanced LEARN --deep)

When `LEARN [company] --deep` or auto-signal on 3+ rejections:

```bash
node lib/career-ops/analyze-patterns.mjs --summary
```

This cross-references ALL tracked applications and returns:

| Dimension | What It Tells You |
|-----------|------------------|
| `archetypeBreakdown` | Which pipe framing converts best across all applications |
| `vendorAnalysis` | Which ATS platforms advance vs block you (Greenhouse vs Workday vs Lever) |
| `scoreComparison` | Average score needed per outcome group |
| `blockerAnalysis` | Most frequent hard blockers (geo, stack, seniority) |
| `remotePolicy` | Remote vs hybrid conversion rates |
| `scoreThreshold` | Data-driven minimum score floor |
| `recommendations` | Top 5 actionable items |

Write result to `reports/pattern-analysis-YYYY-MM-DD.md`. Update `data/learned/pipes.md` with any new archetype/ATS insights.

### Step 6: Propagate to Pipeline

```
SIGNAL pipeline-tracker:
  IF outcome == offer AND accepted → transition to 🏁 ARCHIVED
  IF outcome == offer AND rejected → transition to ❌ REJECTED
  IF outcome == rejection → transition to ❌ REJECTED
  IF outcome == ghosted > 30 days → transition to ❌ GHOSTED
  UPDATE next_action: "Learned from outcome"
```

### Step 7: Propagate to System (General Lessons)

If the lesson is general (not company-specific), update the relevant system component:
- DNA extraction → add/remove keywords
- Positioning framework → adjust archetype guidance
- ATS specs → update format rules
- Kernel rules → add new insight
- Target list → remove similar companies if pattern repeats

---

## Data Files

| File | Purpose | Auto-Create |
|------|---------|-------------|
| `data/learned/[company].md` | Per-company learning file | On first LEARN for this company |
| `data/learned/keywords.md` | Keywords that won/lost interviews | Yes (template exists) |
| `data/learned/skill_gaps.md` | Skills flagged as missing by rejections | Yes (template exists) |
| `data/learned/pipes.md` | Pipe positioning success/fail log | Yes (template exists) |
| `data/learned/salary.md` | Salary data from offers/rejections | Yes (created on first offer) |
| `data/learned/ats_scores.md` | TF-IDF scores per application — corpus for predicting score→outcome by pipe | Yes (created on first ATS-scored LEARN) |

---

## Auto-Learning (Triggered Without Command)

When pipeline signal received:
- ❌ REJECTED → auto-run light LEARN (capture stage + any feedback, no deep analysis)
- 💰 OFFER → auto-run full LEARN (capture what worked + salary data)
- 📞 CALLBACK → auto-log (wait for final outcome before full analysis)
- Ghosted > 30 days → auto-mark as rejection, run light analysis
