---
name: fetch-engine
description: "Triggered when user says FETCH, WIDENET, SCAN, or FETCH --pipe / --urls / --score. SCAN runs career-ops 49-provider auto-scanner. FETCH runs manual board search + SCAN together. Executes continuous 24h-fresh job discovery across all 4 pipes. Every job MUST be posted within last 24 hours of command time. Stale jobs are skipped instantly and replaced from same source. Move like light."
---

# FETCH ENGINE — 8-Phase Job Discovery Pipeline

## Source Truth Anchors (JOBS-OS Primary)
- Full pipeline protocol: `AGENTS.md` → FETCH 8-PHASE PROTOCOL section
- Scoring corpus: `01_MASTER_CORPUS.md`
- ATS rules: `04_ATS_NUANCE_DB.md` + `32_ATS_TECH_SPEC.md`
- Infiltration: `37_INFILTRATION_LAYER.md`
- Consulting DNA: `CONSULTING_OS.md`
- Scripts: `33_FETCH_ENGINE.py`, `APIFY_FETCH.py`
- Exclusions: `data/jobs.json`

## Phase 0 — System Readiness
Before anything else, verify:
1. AGENTS.md loaded — kernel active
2. local_config.json exists — identity ready
3. `data/jobs.json` read — applied jobs excluded (CREATE if not exists: `{"applied":{}, "excluded":[], "last_updated": "YYYY-MM-DD"}`)
4. `data/pipeline/PIPELINE.md` read — already-tracked jobs excluded (CREATE if not exists with template)
5. `data/learned/pipes.md` read — pipe success rates loaded for prioritization
6. Master Corpus accessible — truth anchor set
7. CONSULTING_OS.md accessible — consulting DNA ready
8. secrets.json exists — Apify API key available
9. APIFY_FETCH.py exists — JS fallback module loaded
10. OMNI configs synced — all tools see same rules
11. OneDrive path verified — dual-write active
12. Git remote verified — push target live

Show SYSTEM READY banner. If any check fails → warn user and stop.

## Phase 1 — Create Date Folder
- `YYYY-MM-DD/` at system root
- Subdirs: `WAVE_1/`, `WAVE_2/`, `WAVE_3/`, `CALLBACK_READY/`
- DELETE and recreate if exists (fresh start every time)
- NEVER delete `data/jobs.json` — that is permanent system memory

## Phase 2a — Sweep All 41 Sources + Career Pages + Greenhouse (24h fresh window)
- Full source registry: `data/pipeline/SYSTEM_SOURCES.md`
- READ SYSTEM_SOURCES.md first — sweeps all 41 wired job boards via scan.mjs + manual boards
- **Primary boards (all 24)**: Indeed · LinkedIn · Glassdoor · Workopolis · Jooble · Google Jobs · Hiring Cafe · Startup Jobs · Eluta.ca · SimplyHired · Monster Canada · ZipRecruiter · Otta · BCjobs.ca · Wellfound · WorkBC · Crabjobs · VanHiring · RemoteOK · WeWorkRemotely · Himalayas · Remotive · Jobspresso · Working Nomads
- **T PIPE (Tech/Ops Core)**: Clio, Shopify, Amazon, 1Password, Tailscale, DoorDash, SaaS ops — plus SYSTEM_SOURCES.md T pipe list
- **I PIPE (Internal Strategy)**: lululemon, TELUS, corporate strategy, BizOps, RevOps — plus SYSTEM_SOURCES.md I pipe list
- **C PIPE (Consulting)**: EY-Parthenon, Deloitte, EY, KPMG, PwC, Accenture, MBB — plus SYSTEM_SOURCES.md C pipe list
- **S PIPE (Startups)**: Procurify, Ada, funded Vancouver startups, chief of staff roles — plus SYSTEM_SOURCES.md S pipe list
- **Pipe prioritization**: READ `data/learned/pipes.md` — prioritize pipes with highest callback/offer rate. If S pipe has 50% callback rate and C pipe has 0%, allocate more search effort to S.
- Cross-check Greenhouse boards: Brex, Hootsuite, EviSmart, Thinkific, Practice Better
- Test NEW Greenhouse slugs each run: GitLab, Zapier, Notion, Canva, Stripe, HubSpot, etc.
- **career-ops auto-scan**: Runs `node lib/career-ops/scan.mjs` — hits all 41 wired job boards + 40+ ATS company scanners
  → Returns structured `{ title, url, company, location, postedAt }` for each
  → Merge results with manual board search → dedup by URL → unified CURATED stream
  → If `--company [name]` specified, scan single company:
    `node lib/career-ops/scan.mjs --company "[name]"`
- Apify fallback when webfetch returns blank/truncated

## Phase 2b — Deduplicate Across ALL Sources
- For every raw job found across all 41+ job boards + career pages + Greenhouse:
  - Group by: company name + role title + location (fuzzy match — same company + same level = same job)
  - Collapse each group into ONE entry
  - Retain the best source URL (priority: company career page → ATS portal → LinkedIn → primary board → third-party board)
- Track provenances: note which sources found each job (e.g., "Indeed + Google Jobs + Eluta.ca")
- OUTPUT: clean dedup'd list — no job appears more than once

## Phase 2c — ATS Feasibility Check (Per Dedup'd Job)
- For each job, identify company's ATS platform:
  - Known companies: look up `data/pipeline/SYSTEM_SOURCES.md` ATS cross-reference table
  - Unknown companies: check JD URL for ATS signature (greenhouse.io, workday, oraclecloud, lever.co, icims, etc.)
- Cross-reference against ATS Tech Spec rules:
  - **Greenhouse** → ✅ Pass (Liberation Sans 10pt, DOCX, 0.75in margins)
  - **Workday** → ⚠️ Verify (contact info MUST be in body, not header; Arial/Calibri)
  - **Oracle Cloud** → ✅ Pass (Calibri 11pt, DOCX, 0.75in margins)
  - **Lever** → ✅ Pass (Liberation Sans 10pt, DOCX)
  - **ICIMS** → ✅ Pass (DOCX, standard fonts)
  - **SAP SuccessFactors** → ✅ Pass (Calibri 10-11pt, DOCX)
  - **Taleo** → ⚠️ Caution (legacy, test before submit)
  - **BambooHR** → ✅ Pass (standard DOCX)
  - **Unknown** → ⚠️ Flag for manual check (use Calibri 11pt, 0.75in, generic format)
- Flag per job: ✅ ATS PASS / ⚠️ VERIFY / ❌ BLOCKED (with fix)

## Phase 2d — Route Guidance (Best Door for Each Job)
- For each dedup'd job, determine best application route:
  1. **Company career page** (direct feed, no middleman) — best
  2. **ATS direct portal** (Workday/Greenhouse/Oracle direct URL) — second best
  3. **LinkedIn Easy Apply** — only if career page broken/missing
  4. **Primary board** (Indeed/Google Jobs/SimplyHired) — acceptable fallback
  5. **Third-party board** (Workopolis/ZipRecruiter) — lowest priority
- Rule: job found on career page + board → recommend career page. Job only on board → recommend that board.
- Store in: `Apply Via` column per job — one of "Company site" / "ATS portal" / "LinkedIn" / "Indeed" / "Otta" / "Hiring Cafe" / "[Board name]"

## Phase 3 — Auto-Verify All URLs
- HTTP-check every listing (200=active, 404=dead, 403=caution)
- Dead → instantly replace from unculled pool (no permission needed)

## Phase 4 — Backend Due Diligence
- Score fit% against Master Corpus
- Filter: ≥60% fit, $120K+ floor, TEER 0/1, Vancouver/Remote Canada only
- Skip: government jobs (citizenship required), licensed roles (P.Eng, CPA, MD, RN), credit check roles
- Check `data/jobs.json` — exclude already-applied
- Check `data/pipeline/PIPELINE.md` — exclude already-SHOT or already-SUBMITTED
- Quality gate: established companies only (no sketchy domains/startups with broken HR)

## Phase 4b — Deep Company Scan (Top Targets)

**AUTO-RUN deep_scan.py as step 1 of Phase 4b** (no manual command needed):

1. **Auto-run scanner**: Execute `python3 skills/fetch-engine/scripts/deep_scan.py` (with `PLAYWRIGHT_BROWSERS_PATH=/home/aryan/.agent-browser/browsers PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` env vars). This uses crawl4ai (stealth browser + JS rendering) to scrape ALL open roles from 20+ target career pages. Scan runs in background — proceed with other pipeline phases while it completes.
   - Supports `--pipe C|T|I|S` to filter by pipe
   - Supports `--output-dir YYYY-MM-DD/WAVE_1/` to write directly to date folder
   - If Chrome binary is unavailable (phone mode), skip auto-scanner and fall back to board-based scan

2. **Ingest results**: Read `deep_scan_YYYY-MM-DD.json` and `curated_injection.md` from the output directory. Extract:
   - All fitting roles with fit scores
   - 🔥 hot company flags (companies with 2-3+ fitting roles → +3-5% priority boost)

After Phase 4 produces the scored/filtered job list, deep-scan the highest-fit companies:

1. **Select targets**: Take the top ~10 companies by fit score from the filtered list. Also include any company where a job scored ≥75% fit.
2. **Open career page**: Navigate directly to the company's career page URL (from `data/pipeline/SYSTEM_SOURCES.md` Deep Scan section) or find their career portal via the ATS domain (greenhouse.io, workday.com, etc.).
3. **Scrape ALL open roles** from that career page — not just what job boards returned.
4. **Cross-check each role** against the same filters:
   - $120K+ floor (or estimate from level + market data)
   - TEER 0/1
   - No domain pivot (NO DOMAIN PIVOT HARD RULE)
   - Fit ≥ 60% against Master Corpus
   - Vancouver/Remote Canada
   - No credit check, no heavy quant
5. **Score each role** (fit%) using same Master Corpus cross-ref
6. **Flag companies with 2-3+ fitting roles** — these get a priority boost (more shots on goal = higher ROI):
   - 2 fitting roles → +3% to overall company priority
   - 3+ fitting roles → +5% to overall company priority
7. **Attach role list** to the company entry in CURATED output:
   - Format: `🔥 Company (N roles) — Role1, Role2, Role3 — $SalaryRange — FitScore`
   - Show all discovered roles in the company's pipe section

**Exception**: If the career page is behind a login wall, JS-heavy and unresolvable via webfetch, or returns no matching roles, skip the company gracefully — no time wasted.

**Storage**: Log deep-scan results to `YYYY-MM-DD/WAVE_1/deep_scan_[company].md` per company for reference during SHOOT.

## Phase 5 — Write CURATED_30.md + FETCH_LOG.md
- 30 jobs, pipe-divided (C | T | I | S), sorted by fit% desc
- Each row: #, Pipe, Wave, Company, Role(s), Salary Range, Fit%, ATS Feasibility, Apply Via, Sources, Archetype, Status, Role Count Badge (🔥 if 2-3+ fitting roles)

## Phase 6 — Generate CALLBACK_READY/ DNA Sheets
- One-pager per company: DNA, 60-sec pitch, 5 Q&A, 3 STAR, keywords, outreach
- Contact method column: Phone / Email / Portal (with user sleep-schedule notes)

## Phase 7 — Write New Jobs to Pipeline
For every new job discovered (not in pipeline, not in jobs.json):
```
WRITE to data/pipeline/PIPELINE.md:
  ADD row: [company] | [role] | [salary] | [pipe] | 🟢 LIVE | [today] | — | "Awaiting SHOOT"
```

## Phase 8 — Display
1. Full proofread table with columns: pipe, wave, company, role, salary, fit%, ATS feasibility (✅/⚠️), apply via, sources found on, why
2. Pipeline integration readout: "N new jobs added to pipeline. M jobs already tracked."
3. Simplest Summary — 3-4 sentence plain-language recap (include total # of raw jobs found across 41+ sources before dedup)
4. Command footer — full command reference

## Phase 9 — SHOOT All Jobs (Auto-Trigger)
- Immediately after display, for EVERY unsHOT job:
  - If Tier 1 (Trust): auto-generate 16-section, show summary, ask "BATCH approve?"
  - If Tier 2 (Normal): generate and show full 16-section for proofreading
  - If Tier 3 (Strategic): generate and show full 16-section + "Strategy: discuss [X]"
- One by one, full depth

## Output
- Table + summary + footer in chat
- Files in `YYYY-MM-DD/{WAVE_1,WAVE_2,WAVE_3,CALLBACK_READY}/`
- Pipeline file updated with 🟢 rows
- Dual-write to OneDrive
- Git push (placeholders only)
