# ABHIMANYU 2.0 — 360° System View (Post-Upgrade)

```
                          ╔═══════════════════╗
                          ║   🧠 YOU         ║
                          ║  (The Thinker)   ║
                          ║  Decide · Review  ║
                          ║  YES or NO only   ║
                          ╚═════════╤═════════╝
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              ┌─────▼─────┐  ┌──────▼──────┐  ┌─────▼─────┐
              │  FETCH    │  │  SHOOT      │  │  TRACK    │
              │ "scan"    │  │ "package"   │  │ "status"  │
              └─────┬─────┘  └──────┬──────┘  └─────┬─────┘
                    │               │               │
              ┌─────▼───────────────▼───────────────▼─────┐
              │            DAEMON (Autonomic)              │
              │    Orchestrates all 23 skills on loop      │
              └─────────────────┬─────────────────────────┘
                                │
```

---

## WATERFALL 1 — FETCH ENGINE (QBIT 1 & 2)

```
   YOU: "FETCH"
         │
         ▼
   ┌─────────────────────────────────────────────────────────────────────┐
    │  LAYER 1 — BOARD SCAN (41+ sources)                                │
   │                                                                     │
    │  14 original: Indeed · LinkedIn · Glassdoor · Workopolis · Jooble   │
    │               Google Jobs · Hiring Cafe · Startup Jobs · Eluta.ca   │
    │               SimplyHired · Monster CA · ZipRecruiter · Otta        │
    │               BCjobs.ca                                             │
    │                                                                     │
    │  6 new:      Wellfound · WorkBC · Crabjobs · VanHiring             │
    │              RemoteOK · WeWorkRemotely                              │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 2 — COMPANY CAREER PAGE SCAN (60+ companies)                │
   │  Organized by pipe → sector tiers → priority circles                │
   │                                                                     │
   │  T PIPE (Tech): FAANG → US-in-Canada → Canadian Tech → Scale-ups   │
   │  C PIPE (Consulting): MBB → Big4 → Boutique → Tech-adjacent        │
   │  I PIPE (Corporate): Telco → Retail → Healthcare → Energy → Gov    │
   │  S PIPE (Startups): $50M+ → $10-50M → <$10M                        │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 3 — ATS PROVIDER AUTO-SCAN (49 providers)                   │
   │                                                                     │
   │  lib/ats-providers/_registry.mjs → maps company name → ATS type    │
   │                                                                     │
   │  greenhouse.mjs  → boards-api.greenhouse.io JSON                   │
   │  ashby.mjs       → jobs.ashbyhq.com API                            │
   │  lever.mjs       → api.lever.co/v0/postings                        │
   │  workday.mjs     → *.wd3.myworkdayjobs.com API                     │
   │  successfactors.mjs → careers.*.com (Playwright fallback)          │
   │                                                                     │
   │  Unknown ATS → falls back to generic web scrape via Apify           │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 4 — MULTI-LEVEL SCAN STRATEGY                              │
   │                                                                     │
   │  Level 1: Local parser — check cache, previously seen jobs         │
   │  Level 2: Playwright — JS-rendered career portals                  │
   │  Level 3: HTTP JSON API — direct ATS API calls (fastest, richest)  │
   │  Level 4: WebSearch fallback — when structured sources fail        │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 5 — ADVANCED FILTERS (lib/fetch-filters.mjs)               │
   │                                                                     │
   │  Title filter:    ops/strategy/director/vp → pass                   │
   │                   engineer/sales/support → block                    │
   │  Content filter:  checks JD body when API returns it               │
   │  Location filter: Vancouver/Remote Canada → pass                   │
   │                   Ontario/US/international → block                  │
   │  Salary filter:   $80K-$350K CAD only                               │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 6 — GHOST JOB DETECTION (lib/ghost-detection.mjs)          │
   │                                                                     │
   │  Staleness:  >90 days → ⚠️ stale                                   │
   │  Repost:     same title, new date → ⚠️ suspicious                   │
   │  Liveness:   URL HEAD check → 404 = dead                            │
   │  Freeze:     company news → hiring freeze/layoffs flagged           │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  LAYER 7 — DEDUP + ATS FEASIBILITY + ROUTE GUIDANCE               │
   │                                                                     │
   │  Dedup: same job on multiple sources → collapsed to one entry      │
   │  ATS check: per-job feasibility (✅/⚠️) based on ATS platform       │
   │  Route: company site > ATS portal > LinkedIn > board                │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
                   ┌───────────────────────┐
                   │  OUTPUT: CURATED LIST  │
                   │  5-30 targets          │
                   │  Sorted by TICS pipe   │
                   │  Fit score descending  │
                   │  ATS-feasibility-      │
                   │  ghost-checked         │
                   └───────────┬───────────┘
                               │
                   YOU: "SHOOT [company]"
```

---

## WATERFALL 2 — SHOOT PACKAGE (QBIT 3-5)

```
   YOU: "SHOOT [Company Name]"
         │
         ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 1 — COMPANY SCOUT                                            │
   │  Scrape ALL open roles at company → show in table                  │
   │  Highlight best 3 for Aman                                         │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 2 — HIRING PROCESS REVEAL                                    │
   │  Stage-by-stage: phone screen → case → panel → offer               │
   │  Duration estimates, tips, what they test                          │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 3 — LIVE INTELLIGENCE ALCHEMY                                │
   │  Gather: Glassdoor reviews + Crunchbase + LinkedIn + news          │
   │  Cross-reference: company DNA × Aman's profile × live intel        │
   │  Output: semantic secret — the ONE angle for this company           │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 4 — PIPE SELECTION (Dynamic)                                 │
   │  Read company DNA → choose pipe (S/T/I/C)                          │
   │  Blend if straddles pipes                                          │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 5 — 100% CONTACT DISCOVERY (lib/contact-discovery.mjs)      │
   │                                                                     │
   │  Tier HM: Hiring Manager (direct supervisor)                        │
   │  Tier SR: Senior Recruiter (screening process)                      │
   │  Tier TP: Team Peer (cultural insight)                              │
   │  Tier EX: Executive (strategic context)                             │
   │                                                                     │
   │  Generates: contact names + titles + LinkedIn URLs + outreach msg   │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 6 — WRITE 16-SECTION PACKAGE                                 │
   │  (Section 1-16: header, alignment, scout, process, DNA, ATS,       │
   │   resume text, cover letter, outreach, cheat sheet, checklist,     │
   │   cadence, finops, quality gates, case semantic case)              │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 7 — RECRUITER SIMULATION QA GATE (Silent)                   │
   │  Mock 200+ resumes → 6-second rule → YES/MAYBE/NO                 │
   │  If MAYBE/NO: rewrite narrative layer, re-simulate until YES       │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 8 — EVAL GATE (10 Dimensions)                               │
   │  lib/eval-v2.mjs + eval/EVAL_V2_CRITERIA.md                        │
   │                                                                     │
   │  D1  Role Fit         (×2.0)    — Does Aman's exp match?           │
   │  D2  CV Match         (×1.0)    — Resume tailored?                  │
   │  D3  Level Strategy   (×1.0)    — Right level?                     │
   │  D4  Comp Research    (×1.0)    — Salary benchmarks done?           │
   │  D5  Personalization  (×1.0)    — Company-specific tailoring?       │
   │  D6  Interview Prep   (×1.5)    — Process known?                    │
   │  D7  Co Trajectory    (×0.5)    — Growing/stable/declining?         │
   │  D8  Team Quality     (×0.5)    — Glassdoor reviews?                │
   │  D9  Location         (×0.5)    — Vancouver/Remote Canada?          │
   │  D10 Ghost Check      (×0.5)    — Legitimate posting?               │
   │                                                                     │
   │  PASS ≥ 70 → proceed. WARN 50-69 → rewrite sections. FAIL → full   │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
                   ┌───────────────────────────┐
                   │  OUTPUT: PACKAGE + EVAL   │
                   │  Quality dashboard shown  │
                   │  Triple-written to:       │
                   │  Linux · OneDrive · GitHub│
                   └───────────┬───────────────┘
                               │
                   YOU: "YES" or "NO"
```

---

## WATERFALL 3 — DEPLOY (QBIT 6-8)

```
   YOU: "YES"
         │
         ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 1 — GEN DOCX (gen_docx.py)                                  │
   │  Font + margins per company's ATS platform                        │
   │  Language registry woven in                                        │
   │  Content integrity check (≥20 lines threshold)                     │
   │  Output: Aman_[Company]_[Role]_Resume.docx + Cover_Letter.docx     │
   │  Writes to OneDrive only (date/company/ folder)                    │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 2 — SUBMISSION BLUEPRINT                                     │
   │                                                                     │
   │  ┌─── LAPTOP MODE (T480/T440p) ──────────────────────────┐         │
   │  │  scripts/auto_apply.py --company X                     │         │
   │  │  browser-use opens Playwright → fills → uploads → submit│       │
   │  └───────────────────────────────────────────────────────┘         │
   │                                                                     │
   │  ┌─── PHONE MODE (S25U) ────────────────────────────────┐          │
   │  │  scripts/auto_apply.py --company X --manual            │         │
   │  │  Generates field-by-field blueprint for phone browser  │         │
   │  │  You fill 5 fields → upload → submit → "SUBMITTED"    │         │
   │  └───────────────────────────────────────────────────────┘         │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 3 — NETWORKING CADENCE AUTO-START                            │
   │                                                                     │
   │  T+0  → LinkedIn connect to Hiring Manager                         │
   │  T+3  → Follow-up/engage with Recruiter                            │
   │  T+7  → Value-add note to Team Peer (share relevant article)       │
   │  T+14 → Check-in nudge to Hiring Manager                           │
   │  T+28 → Final close to Executive                                   │
   │                                                                     │
   │  Each message is SEMANTICALLY PERSONAL — woven from live intel     │
   │  System never forgets — cadence footer shown after EVERY response  │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 4 — PIPELINE UPDATE                                          │
   │  Auto-adds to data/pipeline/PIPELINE.md                            │
   │  Stage: ✅ SUBMITTED → T+0 timer starts                            │
   │  Trackable via "TRACK" command at any time                         │
   └───────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
   ┌─────────────────────────────────────────────────────────────────────┐
   │  STEP 5 — POST-SUBMIT INTELLIGENCE                                 │
   │                                                                     │
   │  CALLBACK → interview-prep skill loaded                            │
   │  OFFER → negotiation-playbook loaded (NEGOTIATE [co] [offer])      │
   │  REJECTION → feedback-engine runs (LEARN [co] [outcome])           │
   │  GHOSTED > 30d → auto-closed, system learns                         │
   └─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  LOOP BACK TO FETCH  │
                    │  System is infinite  │
                    │  but not circular    │
                    │  Every cycle smarter │
                    └──────────────────────┘
```

---

## SYSTEM ARCHITECTURE — All Files & Their Purpose

```
ABHIMANYU-2.0/
│
├── AGENTS.md                         ← Kernel rules + boot sequence (THE LAW)
├── MASTER_USER_MANUAL.md             ← Full manual for Aman
├── COMMANDS.md                       ← Command reference
├── BIRDS_EYE.md                      ← THIS FILE — 360° system view
├── SKILL_REGISTRY.md                 ← All 23 skills indexed
│
├── data/
│   ├── pipeline/
│   │   ├── SYSTEM_SOURCES.md         ← ★ EXPANDED — 41+ boards, 80+ companies, 49 ATS
│   │   ├── PIPELINE.md               ← Live kanban of all applications
│   │   └── jobs.json                 ← Machine-readable pipeline
│   ├── system/
│   │   ├── ATS_ESOTERICA.md          ← ★ EXPANDED — 20+ ATS platforms with insider tips
│   │   └── ATS_tech_specs.md         ← Formatting specs per ATS
│   ├── networking/
│   │   ├── CADENCE_FOOTER.md         ← Auto-updating cadence display
│   │   ├── NETWORKING_TRACKER.md     ← Full networking tracker
│   │   └── cadence.json              ← Machine-readable cadence
│   ├── fit_maps/[company].md         ← Permanent ontological fingerprints
│   ├── learned/[company].md          ← Accumulated lessons from outcomes
│   ├── thought_log/YYYY-MM-DD.md     ← Immutable thought journal
│   └── rankings/TICS_PRIORITY.md     ← Priority ladder
│
├── lib/
│   ├── ats-providers/                ← ★ NEW — 49 ATS provider modules
│   │   ├── _registry.mjs             ← Maps 40+ companies → ATS type
│   │   ├── _http.mjs                 ← HTTP transport helpers
│   │   ├── _types.js                 ← Type definitions
│   │   ├── greenhouse.mjs            ← Greenhouse boards-api scanner
│   │   ├── ashby.mjs                 ← Ashby API scanner
│   │   ├── lever.mjs                 ← Lever API scanner
│   │   ├── workday.mjs               ← Workday API scanner
│   │   └── successfactors.mjs        ← SuccessFactors scanner
│   ├── fetch-filters.mjs             ← ★ NEW — Title/content/loc/salary filters
│   ├── ghost-detection.mjs           ← ★ NEW — Staleness/repost/freeze checks
│   ├── contact-discovery.mjs         ← ★ NEW — 4-tier contact finder
│   ├── eval-v2.mjs                   ← ★ NEW — 10-dimension EVAL engine
│   └── career-ops/                   ← Original career-ops (preserved intact)
│
├── scripts/
│   ├── gen_docx.py                   ← DOCX generator (content-integrity guarded)
│   └── auto_apply.py                 ← ★ NEW — browser-use AUTO-APPLY wrapper
│
├── skills/
│   ├── fetch-engine/SKILL.md         ← FETCH command skill
│   ├── shoot-deployer/SKILL.md       ← SHOOT command skill
│   ├── resume-evaluator/SKILL.md     ← EVAL command skill
│   ├── daemon/SKILL.md               ← DAEMON skill (background loop)
│   └── ... (19 more skills)
│
├── eval/
│   ├── OPS_EVAL_CRITERIA.md          ← Original resume eval (preserved)
│   └── EVAL_V2_CRITERIA.md           ← ★ NEW — 10-dimension criteria
│
├── docs/
│   └── UPGRADE_PLAN.md               ← ★ NEW — Full upgrade documentation
│
├── .venv/                            ← ★ NEW — Python venv (browser-use + Playwright)
│
└── JOBS-OS-2026/                     ← Original vault (preserved intact)
    └── 01_MASTER_CORPUS.md           ← Truth anchor for all claims
```

---

## DATA FLOW — What Happens Per Command

```
"FETCH"
  → layer 1: 41+ boards → raw jobs
  → layer 2: 60+ company pages → raw jobs
  → layer 3: 49 ATS providers → structured jobs
  → layer 4: multi-level scan (Playwright → API → fallback)
  → layer 5: advanced filters → collapse
  → layer 6: ghost detection → flag/remove
  → layer 7: dedup + ATS feasibility + route guidance
  → YOU GET: curated table (5-30 targets, sorted by pipe+fit)

"SHOOT [co]"
  → company scout → all roles at company
  → hiring process reveal → stage-by-stage
  → live intel alchemy → semantic secret
  → pipe selection → dynamic (S/T/I/C)
  → contact discovery → 4 tiers of people
  → write 16-section package
  → recruiter simulation (silent QA)
  → EVAL v2 (10 dimensions) → PASS/WARN/FAIL
  → YOU GET: complete package + quality dashboard

"YES"
  → GEN DOCX → ATS-optimized Word docs
  → Submission blueprint → laptop auto or phone manual
  → Networking cadence auto-starts → T+0 timer
  → Pipeline auto-updates
  → Triple-write → Linux + OneDrive + GitHub

"AUTO-APPLY [co]"
  → Detects T480 (browser-use) or phone (fallback)
  → [Laptop] Playwright opens → fills → uploads → submits
  → [Phone] Generates 5-min blueprint → you submit
  → Records in pipeline → cadence continues

"TRACK"
  → Reads data/pipeline/PIPELINE.md
  → Shows live kanban sorted by stage (SUBMITTED → OFFER → REJECTED)

"CADENCE"
  → Reads data/networking/NETWORKING_TRACKER.md
  → Shows every company, every leg, who replied, what's due

"LEARN [co] [outcome]"
  → Rejection → update keywords/positioning/archetype
  → Offer → record winning formula
  → System evolves → next FETCH is smarter
```

---

## WHAT CHANGED (Pre vs Post Upgrade)

| Dimension | Before | After |
|-----------|--------|-------|
| Job boards | 13 | 41+ |
| Company career pages | 30 | 60+ (tiered by sector) |
| ATS platforms known | 6 | 20+ |
| ATS provider modules | 0 | 49 (auto-scan capable) |
| Scan strategy | webfetch only | Multi-level (Playwright → API → fallback) |
| Job filters | Manual (QBIT 2 rules) | Automated (lib/fetch-filters.mjs) |
| Ghost detection | None | Staleness + repost + freeze + liveness |
| EVAL dimensions | 4 | 10 (A-F scoring) |
| Contact discovery | Manual per SHOOT | Automated 4-tier (lib/contact-discovery.mjs) |
| AUTO-APPLY | Phone-only blueprint | Laptop (browser-use) + Phone (blueprint fallback) |
| Pipeline tracking | Basic | Dedup + merge + health checks |
| Everything preserved | ✅ | ✅ Additive-only, zero deletions |

---

## THE ONE-SENTENCE SUMMARY

```
18 boards + 60 companies + 49 ATS providers + 10-dim EVAL + ghost detection
+ contact discovery + browser-use AUTO-APPLY + 20 ATS platforms = system
that scans deeper, filters smarter, fills automatically, and never misses.

YOU still decide. YOU still review. YOU still say YES or NO.
Everything else is machine work.
```
