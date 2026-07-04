---
name: shoot-deployer
description: "Triggered by SHOOT [company], SHOOT [company] --all [roles], or paste JD. Before generation: reads data/learned/ for relevant lessons + data/pipeline/ for existing tracking. After generation: writes to data/pipeline/PIPELINE.md. After YES: transitions pipeline to ✅, auto-starts networking timer, generates DOCX. Full 16-section depth, cross-skill wired."
---

# SHOOT DEPLOYER — Full 16-Section Application Package

## Cross-Skill Wiring (Auto-Executed)

### Before Generation (Data Inputs)
```
Step A1: READ data/pipeline/PIPELINE.md
  → Check if this company/role already tracked
  → If already SHOT/SUBMITTED → warn user, ask if resubmit

Step A2: READ data/learned/ for relevant lessons
  → READ data/learned/pipes.md — find success/fail for this pipe
  → READ data/learned/[company].md if exists — company-specific lessons
  → READ data/learned/keywords.md — keywords that won/lost for similar roles
  → READ data/learned/skill_gaps.md — flagged gaps for this company/pipe
  → INJECT lessons into section generation (DNA, keywords, archetype)

Step A3: CALCULATE trust tier
  → Tier 1 (Trust): fit ≥85% AND familiar pipe AND salary listed AND past success in pipe
  → Tier 2 (Normal): fit 70-84% OR unfamiliar pipe OR no salary data
  → Tier 3 (Strategic): fit <70% OR new company type OR confusing JD
  → SHOW tier in output header
```

### During Generation (Quality Gates — Auto-Executed After Section Gen, Before Output)

```
Step G0: RESUME + COVER LETTER EVAL (Content Substance Check — Runs FIRST)
  → LOAD OPS_EVAL_CRITERIA.md for resume scoring criteria
  → LOAD COVER_LETTER_EVAL_CRITERIA.md for cover letter scoring criteria
  → EVAL Resume (Section 9):
      Score across 4 dimensions:
        scaling_narrative  (0-35) — growth arc, trajectory, scope increase
        strategic_impact   (0-30) — P&L, board, M&A, transformation
        operational_depth  (0-25) — systems built, tech led, teams managed
        domain_alignment   (0-10) — company language, pipe positioning, archetype
      Bonus (max 20): +5 quantified exit, +3 MBA applied, +2 cross-industry, +2 border, +3 builder, +2 tech lead, +1/ea board
      Deductions: -5 immigration/PR, -3 per vague bullet, -2 per missing metric, -3 archetype drift, -3 weak summary
    → PASS (≥70): proceed
    → WARN (50-69): rewrite flagged sections, re-EVAL until PASS
    → FAIL (<50): full rewrite from scratch, re-EVAL until PASS
  → EVAL Cover Letter (Section 11):
      Score across 3 dimensions:
        company_alignment  (0-40) — DNA mirroring, language registry density, insider intelligence
        narrative_flow     (0-30) — arc, authenticity, specificity to company
        format_tone        (0-20) — header correctness, archetype consistency, anti-pattern compliance
      Deductions: -5 generic opening, -3 per unsupported claim, -3 archetype drift, -5 immigration/PR
    → PASS (≥35/90): proceed
    → WARN (25-34): rewrite flagged sections, re-EVAL until PASS
    → FAIL (<25): full rewrite from scratch, re-EVAL until PASS
  → Output EVAL scores into QUALITY DASHBOARD:
    "Resume EVAL: XX/120 — PASS/WARN/FAIL | Cover Letter EVAL: XX/90 — PASS/WARN/FAIL"
  → This gate is the crystallization point — the alchemy is either ready or it isn't.
    No DOCX is ever generated from raw, untested alchemy.

Step G1: ATS VALIDATION PASS
  → CHECK font family: Liberation Sans 10pt (or ATS-specified font for this platform)
  → CHECK margins: 0.5-1.0 inch all sides
  → CHECK section headers: standard names (Experience, Education, Skills — no custom headers)
  → CHECK file type: DOCX per ATS spec (not PDF for Workday, etc.)
  → CHECK keyword density: 2-4% from Language Registry
  → CHECK section completeness: all 16 sections present
  → PASS if 6/6 checks pass. FAIL if ≥2 fail. WARN if 1 fails.
  → Output: "ATS Validation: ✅ / ⚠️ / ❌" with detail per check

Step G2: BULLET QUALITY UPGRADE
  → Scan every bullet in resume text (section 9) against rules:
    ✓ STAR format: Situation-Action-Result structure
    ✓ Metrics: every bullet has a number (%, $, people, locations, time)
    ✓ Strong verb lead: built, scaled, led, designed, transformed (NOT: responsible for, involved in, helped)
    ✓ Passive → active conversion: "was responsible for" → "led"
  → FLAG bullets missing metrics → list them
  → FLAG bullets leading with weak verbs → list replacements
  → FLAG bullets lacking STAR structure → suggest rewrite
  → Output: "Bullet Quality: N/X pass. ⚠️ bullets missing [metrics/verbs/STAR]"

Step G3: ANTI-PATTERN SWEEP
  → SCAN all 16 sections for weasel words:
    "think outside the box", "synergy", "go-getter", "results-driven", "team player",
    "detail-oriented", "hardworking", "proactive", "self-starter", "excellent communication"
  → SCAN for unsupported claims:
    "transformed X" — does Master Corpus support X? "led Y" — does Corpus mention Y?
    Cross-ref every strong claim against provenance file
  → SCAN for archetype drift:
    Archetype A uses builder verbs (built, constructed, designed, architected)
    Archetype B uses operator verbs (managed, optimized, streamlined, executed)
    Archetype C uses strategist verbs (analyzed, planned, advised, directed)
    If selected archetype is A but bullets use strategist verbs → FLAG
  → SCAN for repetition gaps:
    "managed operations" appearing 3+ times across different sections
    Skills listed but never demonstrated in experience bullets
  → Output: "Anti-Patterns: N found. ❌ duplicates / unsupported / drift / gaps"

Step G4: QUALITY DASHBOARD (Summarize All Three)
  → Show single block at the end:
    ┌──────────────────────────────────────────┐
    │ 📋 QUALITY DASHBOARD                     │
    │ ATS Validation:    ✅ (6/6)              │
    │ Bullet Quality:    ⚠️ (14/18)           │
    │ Anti-Patterns:     ❌ 3 found            │
    │ Semantic Enrich:   ✅ JSON-LD generated  │
    │ Fix before submit? → ────────────        │
    └──────────────────────────────────────────┘
  → If any gate fails: list specific fixes, numbers, exact replacements
  → AUTO-FIX: for bullet quality and anti-patterns, generate corrected versions
  → User sees: raw output + quality dashboard + auto-fixed suggestions

Step G5: SEMANTIC ENRICHMENT (JSON-LD Generation)
  → RUN: python3 scripts/semantic_enricher.py
       --company "[company]" --role "[role]"
       --skills "[pipe keywords from Language Registry]"
       --pretty --output "2026-XX-XX/semantic/[company]_[role]_ld.json"
  → Generates schema.org/Person JSON-LD block
  → Attached alongside DOCX for next-gen ATS platforms
  → Output appears in QUALITY DASHBOARD as "Semantic Enrich" line
  → No user-facing change — this is invisible enrichment for machines
```

### After Generation (Data Outputs)
```
Step B1: WRITE to data/pipeline/PIPELINE.md
  → ADD row: [company] | [role] | [salary] | [pipe] | 🔵 SHOT | [today] | T+0 | "Awaiting approval"
  → If --all multi-role: add one row per role
  → If row already exists (resubmit): UPDATE status to 🔵

Step B2: WRITE to data/jobs.json if not exists (create with {})
  → Add to applied.exclusion list for this company (so FETCH skips it)

Step B3: WRITE quality report to data/pipeline/PIPELINE.md
  → APPEND quality scores to the pipeline row as metadata

Step B4: DISPLAY output with pipeline row shown + quality dashboard
```

### After User Says YES (Approval → Auto-Trigger Chain)
```
Step C1: TRANSITION pipeline row: 🔵 SHOT → ✅ SUBMITTED
  → WRITE to data/pipeline/PIPELINE.md: set stage = ✅, set T+0 = today

Step C2: GENERATE DOCX via document-engine
  → Convert LaTeX resume + cover letter to DOCX
  → Save to date folder

Step C3: AUTO-START networking timer
  → WRITE to data/networking_log.json: company, T+0 date, personas, message templates
  → Networking footer auto-shows cadence from this point

Step C4: Git commit + push

Step C5: SHOW next action: "AUTO-APPLY [company] | AUTO-APPLY --manual (phone)"
```

---

## Source Truth Anchors (JOBS-OS Primary)
- Unified format: `35_UNIFIED_SHOOT_FORMAT.md`
- Infiltration layer: `37_INFILTRATION_LAYER.md`
- ATS specs: `04_ATS_NUANCE_DB.md` + `32_ATS_TECH_SPEC.md`
- Corpus: `01_MASTER_CORPUS.md`
- Resume rules: Tailscale style (AGENTS.md rules section)
- Cover letter rules: AGENTS.md cover letter format section
- Networking: AGENTS.md networking section
- Consulting: `CONSULTING_OS.md`
- Positioning by Pipe: AGENTS.md — POSITIONING BY PIPE FRAMEWORK section
- Multi-Role Limit: AGENTS.md — Multi-Role Application Limit kernel rule
- Learned data: `data/learned/[company].md`, `data/learned/pipes.md`, `data/learned/keywords.md`
- Pipeline: `data/pipeline/PIPELINE.md`
- Jobs log: `data/jobs.json`

## Multi-Role Workflow (Same Company, Multiple Roles)

When applying to 2-3 roles at the same company (see Multi-Role Strategy section 4):

**Shared across all roles:**
- Section 2 (Company Scout) — covers ALL roles at the company
- Section 3 (Hiring Process Reveal) — one per company
- Section 4 (Multi-Role Strategy) — the strategy for THIS company specifically

**Per-role (generated for EACH role):**
- Section 1 (HEADER) — role-specific
- Section 5 (CORE Alignment) — per role
- Section 6 (DNA EXTRACTION) — per role (each JD uses different language)
- Section 7-8 (ATS, Device) — shared (same platform)
- Section 9-12 (Resume, Cover Letter) — independently customized per role
- Section 13 (LinkedIn) — shared personas, role-specific messages
- Section 14-16 (Interview, Checklist, Follow-Up) — per role

**Cover letter cross-reference:** Each cover letter must acknowledge the other application:
> "I've also applied to [other role] because my background bridges both [skill A] and [skill B]. Applying to both demonstrates my genuine interest in [company] and my conviction that I can add value across teams."

**Format:** `SHOOT [company] --all [role1, role2, role3]` generates a single master document with shared sections + per-role variants.

---

## The 16 Sections (Every Job, Every Time)

### 1. HEADER
Company, Role, Team, Salary (range + midpoint), Location, Fit Score, Pipe, Wave, NOC, TEER, Archetype, **Trust Tier**

**Pipe positioning pre-selected:** Run the decision tree from POSITIONING BY PIPE FRAMEWORK in AGENTS.md. Read company DNA → select pipe frame → blend if needed → choose archetype. All 16 sections flow from this selection.

**Archetype locked:** Once selected, this archetype (A/B/C) is enforced across ALL 16 sections. Resume, cover letter, interview script — same archetype. No drift.

### 2. COMPANY SCOUT (All Relevant Roles)
**Permanent constitutional section — kills fear by showing the full landscape.**
- Scout ALL roles at the target company relevant to Aman's profile
- Show in table: Role, Level, Salary, Status (live/stale/shot/below floor)
- Highlight Best 3 with 1-liner why
- Even roles below salary floor are listed (so Aman knows what exists)

### 3. HIRING PROCESS REVEAL (How This Company Hires)
**Permanent constitutional section — kills fear by knowing the script.**
- Stage-by-stage process: what happens, duration, who you meet
- Experienced-hire specific rules (what they skip vs campus recruits)
- Key tips per stage (case interview? behavioral? take-home?)
- Timeline: how long from apply to offer
- What NOT to worry about (psychometric tests? assessment centres?)
- General company hiring philosophy (meritocratic? pedigree-focused? culture-first?)

### 4. MULTI-ROLE STRATEGY + ESOTERIC KNOWLEDGE
**Permanent constitutional section — insider knowledge that only company insiders know. Turns "how many jobs to apply for" from guesswork into strategy.**
- **Count recommendation:** How many roles Aman should apply to at THIS company (1/2/3 ceiling-4). Sources: Scale.jobs says 2-3, Frontline Source says 3-4 over sustained period, CNBC 2026 says multiple apps = desperate unless coherent, Indeed says 1-2 months gap. Consensus: 2-3 optimal, 4 absolute ceiling. Never more.
- **Coherence rule:** Roles must be same level + related function (Sr Mgr Strategy + Sr Mgr M&A = coherent. Sr Mgr Strategy + Analyst = career confusion)
- **Cadence recommendation:** Space X (1 week? 2 weeks?). Don't fire same day. Stagger.
- **ATS insider knowledge:** Does this company's ATS flag multi-applicants positively (shows initiative) or negatively (spray-and-pray)? Does it notify the recruiter? Does it keep rejected candidates in a talent pool?
- **Back-door path:** What's the optimal route — referral, direct apply, recruiter reach-out? Does this company have a generalist pipeline for experienced hires?
- **Rejection cooldown:** 6 months same role, no wait for different role at same company
- **Transparency rule:** If asked in interview, be honest about other applications — frame as genuine interest in the company
- **Cover letter cross-reference (if multi-role):** Each cover letter acknowledges the other application(s).

### 5. CORE Alignment Matrix
One-liner + Table: `JD Requirement → Aman's Map` (what they need → what he's done)

### 6. DNA EXTRACTION
- Company background + market position
- Language Registry (exact words they use — these go into resume at 2-4% density)
- Value System (what they reward)
- Cultural Cues (how they communicate)
- Anti-Patterns (what they hate — never include these)
- **Learned lessons from data/learned/ injected here** (keywords that worked/failed for similar companies)

### 7. ATS SPECS
- Platform (Greenhouse/Workday/Lever/Ashby/etc.)
- Font, Size, Format, Margins, Section Headers, Special Rules
- DOCX per spec, 100% parseable

### 8. DEVICE MAP
- Hardware they issue, OS, peripherals, IT policy, Day 1 prep

### 9. RESUME TEXT (Plain)
- Tailscale style: Name+contact centered, Professional Summary (3-4 sentences), Core Competencies (pipe-separated), Experience (Company — Title | Location, metrics bullets), Education, Technical Proficiency
- LOCAL CANADIAN IN BC framing — no immigration language
- Archetype enforced: resume text matches chosen archetype (A: builder verbs, B: operator verbs, C: strategist verbs)
- In code fence for proofreading

### 10. RESUME LATEX (.tex source)
- Full LaTeX source with proper formatting
- `\textbf{Company} \hfill \textbf{Title}` pattern
- `\begin{itemize}` for bullets
- Liberation Sans 10pt

### 11. COVER LETTER TEXT (Plain)
- 6-paragraph narrative mirroring company DNA
- Archetype enforced: same archetype as resume
- If multi-role: includes cross-reference to the other role(s) applied
- Header: `[NAME]` / Date: DD/MM/YYYY / Vancouver, BC, Canada
- Closing: Best regards, `[NAME]` / Phone: `[PHONE]` / Email: `[EMAIL]` / LinkedIn: `[LINKEDIN]`
- In code fence for proofreading

### 12. COVER LETTER LATEX (.tex source)
- Full LaTeX with mailto + https hyperlinks

### 13. LINKEDIN OUTREACH (4-Tier)
- T+0: Connect + note to IC/Associate
- T+3: Follow-up to Manager/Director
- T+7: Value-add to Sr IC/Manager
- T+14: Final nudge to Exec Sponsor
- Each with full message text + persona rationale

### 14. INTERVIEW CHEAT SHEET
- 60-sec pitch (archetype-locked)
- 5 Q&A with specific answers (not generic)
- 3 STAR stories (Profitability, Credibility, Visibility pillars)
- Keywords to use, anti-patterns to avoid
- "One year from now" question
- Rejection response script

### 15. CHECKLIST (21+ Items)
- DNA extracted? ATS keywords at 2-4%? Title aligned? No immigration language? DOCX ready? etc.
- Company scout completed? Hiring process revealed? Provenance verified? Multi-role strategy defined?
- data/learned/ read? Archetype locked across all sections?
- Pipeline updated? Trust tier assigned?
- **ATS Validation passed?** (font, margins, headers, keywords, file type, sections)
- **Bullet Quality check passed?** (metrics in every bullet, strong verbs, STAR structure)
- **Anti-Pattern sweep done?** (weasel words removed, unsupported claims flagged, archetype consistent, no gaps)

### 16. FOLLOW-UP + FINOPS
- T+0 through T+28 cadence with conditional triggers
- FinOps: negotiation targets, walk-away floor, benefits leverage

## Execution Protocol (Concrete Steps)

### On SHOOT Trigger
```
 1. READ data/pipeline/PIPELINE.md → check for existing entries
 2. READ data/learned/pipes.md + data/learned/[company].md + data/learned/keywords.md
 3. RUN LinkedIn Profile Audit → check alignment with target company/role
 4. CALCULATE trust tier
 5. RUN Semantic Layer (10 questions)
  6. GENERATE 16 sections (with learned lessons injected)
  7. **RUN RESUME + COVER LETTER EVAL (Step G0)** → score resume against OPS_EVAL_CRITERIA.md, score cover letter against COVER_LETTER_EVAL_CRITERIA.md
     → If PASS: continue. If WARN: rewrite flagged sections, re-EVAL. If FAIL: full rewrite from scratch.
     → This is the CRYSTALLIZATION POINT — no DOCX ever ships from raw alchemy.
  8. RUN ATS VALIDATION PASS (Step G1) → check font, margins, headers, keywords, sections
  9. RUN BULLET QUALITY UPGRADE (Step G2) → quantifier scan, verb audit, STAR check
 10. RUN ANTI-PATTERN SWEEP (Step G3) → weasel words, unsupported claims, archetype drift, gaps
 11. RUN SEMANTIC ENRICHMENT (Step G5) → generate JSON-LD for next-gen ATS
 12. RUN provenance auto-verify (cross-ref every claim with Master Corpus)
 13. SHOW QUALITY DASHBOARD (Step G4) — gates summary + EVAL scores + auto-fix suggestions
 14. SHOW full 16-section in chat (with trust tier + quality dashboard + EVAL verdict + provenance pass/fail)
 15. SHOW LinkedIn Audit output (aligned/misaligned items)
 16. WRITE row to data/pipeline/PIPELINE.md (🔵 SHOT) with quality scores
 17. WRITE to data/jobs.json (company added to exclusion)
 18. WRITE JSON-LD to date folder (semantic enrichment — machine use only)
```

### On YES (Approval) — Auto-Trigger Chain
```
⛔ PRE-FLIGHT CHECK: EVAL must have PASSED on both resume and cover letter
  → If EVAL was never run or scored WARN/FAIL → BLOCK. "Run EVAL first. Cannot generate DOCX from untested alchemy."
  → If EVAL passed → proceed.

1. TRANSITION data/pipeline/PIPELINE.md: 🔵 → ✅, set T+0 = today
2. GENERATE DOCX via document-engine
3. WRITE to data/networking_log.json: auto-start cadence (T+0/3/7/14)
4. Git commit + push
5. DISPLAY: "Ready for AUTO-APPLY. | Phone mode: AUTO-APPLY --manual"
```
