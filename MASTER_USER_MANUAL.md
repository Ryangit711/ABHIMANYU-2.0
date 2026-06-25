# ABHIMANYU 2.0 — MASTER USER MANUAL

**Aman's complete operator's guide.**  
*The system does the typing. You do the thinking.*

---

## HOW THIS SYSTEM WORKS (30-Second Summary)

ABHIMANYU is a job-search operating system. You say a command. I load the right skill, execute it with full depth, present output for your review, and push everything to git. Your only jobs: **Decide**, **Review**, **Say YES or NO**.

```
YOU:  FETCH → picks targets → YOU: SHOOT [company] → I write package → YOU: YES
      → I auto-apply → networking timer starts → YOU: wait for callback
      → callback → interview prep → YOU: interview → offer → negotiation → 💰
```

---

## QUICK START — First Session

```
1. FETCH              → I scan 13+ sources for 24h-fresh jobs
2. Review the table    → pick a company
3. SHOOT [company]     → I write the full 16-section package
4. Review the package  → if good, say YES
5. YES                 → I auto-start networking timer
6. AUTO-APPLY [co]     → I submit the application
7. CADENCE             → see networking tracker with T+ legs
```

---

## COMPLETE COMMAND REFERENCE

### 🔍 Discovery & Intelligence

| You Say | What Happens |
|---------|-------------|
| `FETCH` | Scans 13+ job boards across all 4 pipes (Consulting, Tech, Internal, Startup). Returns only jobs posted in the last 24h. Deduped, ATS-checked, scored. |
| `WIDENET` | Expanded FETCH — broader sources, deeper drill. |
| `ATOMIZE [paste JD]` | Extracts company DNA from a job description — language registry, value system, archetype, fit score. |
| `SCORE [jd_text]` | Scores a job description against Aman's profile (TF-IDF cosine similarity). |
| `DISTILL [topic/url]` | Harvests social intelligence — Reddit threads, Instagram saved posts, LinkedIn intel. |
| `STATUS` | Org health check — all 22 skills, last run, freshness. |
| `DIAGNOSE` | Full 10-phase system diagnostics. |
| `REFRESH` | Re-scan all pipes, replace stale jobs with fresh ones. |
| `AUDIT` | Full system health — skill freshness, TICS pipe coverage, pipeline health. |
| `AUDIT --skills` | Skill freshness check only. |
| `AUDIT --coverage` | TICS pipe coverage only. |
| `AUDIT --pipeline` | Pipeline health only. |

### 🎯 Targeting & Approval

| You Say | What Happens |
|---------|-------------|
| `SHOOT [company]` | Writes complete 16-section package: header, alignment, scout, process, DNA, ATS, resume, cover letter, LinkedIn outreach, interview cheat sheet, checklist, cadence, finops, quality gates, semantic case. |
| `SHOOT [paste full JD]` | Same, but from a raw JD paste. |
| `BATCH [co1, co2, ...]` | Batch-approve Trust-tier SHOOTs without full review. |
| `BATCH --all` | Approve ALL pending Trust-tier SHOOTs at once. |
| `YES` | Approve the SHOOT package → auto-starts networking cadence. |

### 📄 Document Generation

| You Say | What Happens |
|---------|-------------|
| `ALCHEMIZE [company]` | Generates ATS-optimized resume + DNA-alchemized cover letter. |
| `OPTIMIZE LINKEDIN [company]` | Runs LinkedIn Profile Audit — headline, about, skills, experience alignment with target role. |
| `LINKEDIN APPLY-AUDIT` | Applies the audit changes via OpenCLI. |

### 🤖 Automation

| You Say | What Happens |
|---------|-------------|
| `AUTO-APPLY [company]` | Launches browser automation — navigates career page, fills forms, uploads resume/cover letter, submits. |
| `AUTO-APPLY --all` | Batch auto-apply to all SHOT/approved jobs. |
| `AUTO-APPLY [company] --manual` | Force manual-submit mode (generates phone-friendly blueprint). |
| `MANUAL-SUBMIT [company]` | Generates exact field-by-field phone submission blueprint with URL, ATS type, field mapping, file bundle, workflow. |
| `BROWSER [command]` | Direct browser-use commands. |

### 🔗 LinkedIn Outreach

| You Say | What Happens |
|---------|-------------|
| `LINKEDIN CONNECT [name]` | Sends LinkedIn connection request via OpenCLI. |
| `LINKEDIN INBOX` | Reads LinkedIn messages. |
| `LINKEDIN SEARCH [query]` | Searches LinkedIn jobs. |
| `CONTACT [name] [title] [company]` | Registers a contact for multi-channel outreach (LinkedIn + email cadence). |

### 📡 Networking Cadence

| You Say | What Happens |
|---------|-------------|
| `CADENCE` | Shows full NETWORKING_TRACKER.md — every company, every leg, who replied. |
| `CADENCE --footer` | Shows live compact footer only. |
| `CADENCE SUBMIT [company]` | Records submission date, starts T+0 → T+28 networking timer. |
| `CADENCE UPDATE [company] [leg] [action]` | Marks a networking leg as `sent`, `replied`, `complete`, or `skipped`. |
| `CADENCE CONTACT [company] [name] [title] [linkedin]` | Adds a contact to the company in the networking tracker. |
| `SUBMITTED [company]` | Legacy command — marks company as submitted, starts cadence. |

### 📊 Pipeline Tracking

| You Say | What Happens |
|---------|-------------|
| `TRACK` | Shows live pipeline kanban — stage, T+ days, next action for every job. |
| `TRACK [company]` | Shows that company's jobs in pipeline. |
| `TRACK --active` | Shows only non-archived jobs. |
| `TRACK --offers` | Shows offers only. |
| `TRACK --stats` | Pipeline metrics — apply rate, callback rate, offer rate. |

### 🧠 Learning & Memory

| You Say | What Happens |
|---------|-------------|
| `THOUGHT [search]` | Searches all thought logs for a keyword. |
| `THOUGHT --today` | Shows today's full thought log. |
| `THOUGHT --last` | Shows last 10 prompts. |
| `THOUGHT --range YYYY-MM-DD YYYY-MM-DD` | Date range search. |
| `THOUGHT --journal` | Exports full journal for external archive. |
| `LEARN [company] [outcome]` | Feeds outcome back into system — rejection, callback, offer. Analyzes why, updates learned files. |
| `LEARN [company] --deep` | Full multi-source analysis (5-10 min). |

### 💰 Offers & Negotiation

| You Say | What Happens |
|---------|-------------|
| `NEGOTIATE [company] [offer]` | Loads negotiation playbook — market range, BATNA, anchoring strategy, multi-offer stalling scripts. |

### 🤖 Autonomous Mode

| You Say | What Happens |
|---------|-------------|
| `LIFTOFF` | Full autonomous cycle — scans all pipes + Reddit/community intel → synthesizes → ranks → presents menu. You pick. I handle the rest. |
| `LIFTOFF --full` | Full cycle including SHOOT + DEPLOY on top-ranked job (prompts for approval at each stage). |
| `DAEMON START` | Starts background auto-loop — rechecks every hour, auto-updates cadence, auto-nudges. |
| `DAEMON STOP` | Stops background auto-loop. |
| `DAEMON STATUS` | Shows loop status, last cycle time, pipeline health. |
| `DAEMON CONFIG` | Shows/sets daemon configuration. |
| `INGEST [url]` | Feeds Instagram/X.com post into social intelligence layer. Extracts → cross-references → reports. |
| `INGEST [url] --assimilate` | Same + queues new intel for system assimilation. |
| `INGEST --queue` | Shows pending assimilations for your review. |
| `INGEST --approve [id]` | Approves a pending assimilation. |

### 🔧 System

| You Say | What Happens |
|---------|-------------|
| `SYNC` | Machine Sync Protocol — propagates AGENTS.md to all AI tool configs, syncs OneDrive. |
| `STATUS` | Shows all 22 skills, their freshness, and system health. |

---

## THE 8-STEP WORKFLOW (Quantum A-Z Framework)

Every application follows exactly 8 steps. Never skip, never reorder.

```
QBIT 1 — EYES SCAN
├── 13+ job boards + company career pages + Greenhouse
├── Collapse duplicates (same job, multiple sources → one entry)
├── ATS feasibility check per job
├── Route guidance: company site > ATS portal > board
└── OUTPUT: raw wavefunction of ALL live jobs

QBIT 2 — COLLAPSE WAVEFUNCTION
├── 24h fresh? → keeps
├── $80K+? → keeps (no ceiling)
├── Vancouver/Remote Canada? → keeps
├── No credit check? → keeps (skip banks/credit unions/insurance)
├── No heavy Excel/quant? → keeps (skip FP&A/data science/pricing)
├── PR-qualifying (TEER 0/1)? → keeps
├── Fit > 6/10? → keeps
└── OUTPUT: CURATED list (5-30 targets)

QBIT 3 — ONTOLOGY MAPPING
├── Read company DNA → what do they sell? → Pipe
├── Read JD verbs → what do they need? → Archetype
├── Map A→C score (Aman vs Company fit)
├── Map C→A score (Company vs Aman value)
├── Store in data/fit_maps/[COMPANY].md (permanent)
└── OUTPUT: ontological fingerprint per target

QBIT 4 — PRIORITY RANKING
├── Priority = (Speed × 0.4) + (Ease × 0.3) + (Pay × 0.3)
├── Sorted ladder → you see → you say SHOOT [X]
└── OUTPUT: data/rankings/TICS_PRIORITY.md

QBIT 5 — SHOOT PACKAGE
├── Load Fit Map + Company DNA + JD Language Registry
├── 16 sections: header, alignment, scout, process, DNA, ATS,
│   resume, cover letter, LinkedIn outreach, interview cheat
│   sheet, checklist, cadence, finops, quality gates, case
├── Every claim traceable to Master Corpus
└── OUTPUT: Complete package for your review

QBIT 6 — GEN DOCX
├── Font: per company ATS
├── Margins: per company ATS
├── Vocab: company language registry woven in
├── Length: company-preferred (1-2 pages)
├── Dual-write: OneDrive (DOCX) + Linux dir (.md)
└── OUTPUT: Aman_[Co]_[Role].docx + Cover_Letter.docx

QBIT 7 — SUBMIT
├── Phone (S25U): MANUAL_SUBMIT blueprint → field-by-field
├── Laptop (T480/T440p): browser-use → auto-fill → auto-submit
└── OUTPUT: Application sent ✅

QBIT 8 — POST-SUBMIT (Living System)
├── PIPELINE.md: auto-update stage
├── jobs.json: record applied + date + pipe
├── networking_log.json: seed T+0/T+3/T+7/T+14 cadence
├── Git: commit + push
├── OneDrive: sync
├── CADENCE RUNS: T+0 LinkedIn connect → T+3 engage
│   → T+7 value-add → T+14 nudge → T+28 close
├── CALLBACK → interview prep
├── OFFER → negotiation playbook
├── REJECT → feedback engine → system learns
└── OUTPUT: System evolved. Loop back to QBIT 1.
```

---

## NETWORKING CADENCE — The 5-Leg System

After every YES, a T+0 timer starts automatically. The system tracks. You act.

| Leg | T+ | Due | Action | Message Type |
|:---:|:--:|:---:|--------|-------------|
| 1 | 0 | Submit day | LinkedIn connect | Connection request (brief note or none) |
| 2 | 3 | Day 3 | Engage | "Enjoyed learning about [initiative]. Impressed by [specific]." |
| 3 | 7 | Day 7 | Value-add | Share article/insight relevant to their work + 1-sentence note |
| 4 | 14 | Day 14 | Nudge | "Still interested. Any updates?" |
| 5 | 28 | Day 28 | Close | "Closing the loop. Happy to reconnect if anything changes." |

**Commands:**
- `CADENCE` — see full tracker
- `CADENCE --footer` — see compact footer
- `CADENCE SUBMIT Indeed` — record submission, start timer
- `CADENCE UPDATE Indeed 2 sent` — mark Leg 2 as sent
- `CADENCE CONTACT Indeed "John" "Recruiter" "https://linkedin.com/in/john"`

---

## FILE SYSTEM MAP

```
ABHIMANYU-2.0/
├── AGENTS.md              ← SYSTEM BRAIN — kernel rules, commands, philosophy
├── MASTER_USER_MANUAL.md  ← THIS FILE — operator's guide
├── README.md              ← Project overview
├── BIRDS_EYE.md           ← Strategic overview, 14 targets ranked
├── SKILL_REGISTRY.md      ← All 22 skills indexed
├── Master_Resume.md       ← Aman's master resume text
├── REFERENCES.md          ← Cross-reference to JOBS-OS source
│
├── skills/                ← 22 skills, each with SKILL.md
│   ├── fetch-engine/      ← Job discovery (13+ sources)
│   ├── shoot-deployer/    ← SHOOT package generator (16-section)
│   ├── dna-extraction/    ← Company alchemy engine
│   ├── resume-writer/     ← ATS-optimized resume builder
│   ├── cover-letter-writer/ ← DNA-alchemized cover letters
│   ├── interview-prep/    ← Callback protocol, 7-stage scripts
│   ├── networking-cadence/ ← Auto-timer (T+0→T+28)
│   ├── salary-negotiation/ ← Comp analysis + negotiation scripts
│   ├── rejection-handler/ ← Graceful reply + system learning
│   ├── thought-log/       ← Immutable prompt journal
│   ├── social-distill/    ← Social intelligence harvesting
│   ├── contact-engine/    ← Multi-channel outreach manager
│   ├── document-engine/   ← DOCX/PDF/XLSX generation
│   ├── system-health/     ← STATUS, DIAGNOSE, REFRESH
│   ├── browser-automation/ ← Auto-apply via browser-use
│   ├── linkedin-automation/ ← OpenCLI LinkedIn adapter
│   ├── pipeline-tracker/  ← Live kanban + AUDIT
│   ├── feedback-engine/   ← Systemic learning loop
│   ├── manual-submit/     ← Phone fallback blueprints
│   ├── negotiation-playbook/ ← Executable negotiation
│   ├── skill-creator/     ← Meta-skill for creating new skills
│   └── daemon/            ← Autonomous nervous system
│
├── scripts/               ← Utility scripts
│   ├── DAEMON.sh          ← Background heartbeat (every 3600s)
│   ├── update_cadence.sh  ← Auto-calculate T+ days & leg status
│   ├── cadence_ctl.sh     ← CADENCE command handler
│   ├── gen_docx.py        ← Parametric DOCX generator
│   ├── gen_master_resume.py ← Master resume DOCX/PDF
│   ├── gen_indeed_docx.py ← Indeed-specific DOCX
│   ├── gen_merged_pdf.py  ← Merge resume + cover letter to PDF
│   ├── ats_scorer.py      ← TF-IDF cosine similarity scorer
│   ├── semantic_enricher.py ← Schema.org JSON-LD generator
│   └── OMNI_SYNC.sh       ← Propagate AGENTS.md to all configs
│
├── data/
│   ├── jobs.json          ← All applied jobs log
│   ├── networking_log.json ← Networking cadence log
│   ├── fit_maps/          ← Company DNA (8 companies)
│   ├── learned/           ← System learning (5 files)
│   ├── networking/        ← Live cadence tracker
│   │   ├── cadence.json   ← Machine-readable data
│   │   ├── CADENCE_FOOTER.md ← Live footer
│   │   └── NETWORKING_TRACKER.md ← Full tracker
│   ├── pipeline/          ← Pipeline kanban + archives
│   ├── daemon/            ← DAEMON logs + evolution data
│   ├── thought_log/       ← Immutable thought journal
│   ├── summary/           ← Session-by-session anchored summaries
│   └── rankings/          ← Priority rankings
│
├── eval/                  ← Test infrastructure
│   ├── agents/            ← 3 grading agents
│   ├── suite/             ← 3 test suites
│   └── viewer/            ← HTML review viewer
│
├── 2026-06-19/            ← Daily output (CURATED, SHOOTs, etc.)
├── 2026-06-20/
├── 2026-06-21/
├── 2026-06-22/
└── 2026-06-24/
```

---

## PIPES — The 4 Positioning Frameworks

| Pipe | When | How to Frame Aman | Salary Band |
|------|------|-------------------|:-----------:|
| **C** — Consulting | Big4, MBB, boutique consulting | Builder-consultant: "I've done what you advise clients to do" | $126K-$234K |
| **T** — Tech/BigTech | SaaS, Big Tech, product companies | Systems builder: "I built the stack, I didn't just use it" | $120K-$200K |
| **I** — Internal Strategy/Corporate | Corporate strategy, program management | Strategy-execution bridge: "I write decks AND implement" | $120K-$180K |
| **S** — Startups | Series A/B, founder-led | Proven builder: "I did the journey you're on" | $120K-$160K + equity |

**One True Pitch (every pipe, every company):**
> "I built something from nothing, scaled it to 70 people and 32 locations, led the technology transformation myself, managed every dollar of the P&L, and delivered a $17M exit. I don't need to learn how your business works — I need to make it work better."

---

## KERNEL RULES (Quick Reference)

| # | Rule | What It Means For You |
|---|------|----------------------|
| 1 | **LIVE INTELLIGENCE ALCHEMY ENGINE** | Every external touchpoint is intelligence-optimized. I research deeply before every message. |
| 2 | **Philosopher's View** | You decide, you review, you say YES/NO. I do the typing. |
| 3 | **Eternal NOW** | The job already exists. No anxiety. Only execution. |
| 4 | **Always build on top** | Nothing is ever deleted. Only added or archived. |
| 5 | **Truth anchor** | Every claim traceable to Master Corpus. No fabrication. |
| 6 | **Privacy** | Git uses `[NAME]`. Personal data never committed. |
| 7 | **Dual-write** | Every file goes to Linux AND OneDrive. |
| 8 | **Push after EVERY prompt** | Auto-push. You never say "push." It is THE LAW. |
| 9 | **Thought journal** | Every prompt logged before response. Immutable. |
| 10 | **24h Fresh Window** | FETCH only returns jobs posted in last 24h. |
| 11 | **Skip credit check roles** | Banks, credit unions, insurance — silently skip. |
| 12 | **Skip heavy quant roles** | FP&A, data science, pricing, advanced Excel — silently skip. |
| 13 | **No immigration language** | Never mention PR/visa/work permit. Frame as local Canadian. |
| 14 | **Full depth** | 16-section SHOOT, no shortcuts. |
| 15 | **Multi-role limit** | 2-3 per company, 4 ceiling. Space 1-2 weeks apart. |

---

## STATUS ICONS

| Icon | Meaning |
|:----:|---------|
| 🟢 | LIVE — job is active in pipeline |
| 🔵 | SHOT — selected, package ready or pending |
| ✅ | SUBMITTED — application sent |
| 📞 | CALLBACK — interview stage |
| 💰 | OFFER — money on the table |
| ❌ | REJECTED — closed, learning captured |
| ⏸️ | PAUSED — waiting on prior step |
| 🟡 | SENT — networking message sent |
| 🔴 | OVERDUE — past due date, action needed |
| ⏳ | FUTURE — not yet due |
| 🔍 | NEEDED — research required |

---

## WHAT TO DO WHEN...

| Situation | Action |
|-----------|--------|
| **Starting a session** | Say `STATUS` to see where everything stands. Then `CADENCE` to check networking. |
| **Need fresh jobs** | `FETCH` — returns only last 24h. |
| **Found a company I want** | `SHOOT [company name]` or paste the JD. |
| **Package looks good** | Say `YES` — auto-starts cadence, readies auto-apply. |
| **Need to submit** | `AUTO-APPLY [company]` (laptop) or `AUTO-APPLY [company] --manual` (phone). |
| **Need to network** | `CADENCE` to see what's due. Then `LINKEDIN CONNECT [name]` to send requests. |
| **Got a callback** | Just tell me — I load interview prep. |
| **Got an offer** | Say `NEGOTIATE [company] [amount]` — I load the playbook. |
| **Got rejected** | Tell me — I analyze why and make the system smarter. `LEARN [company] rejected`. |
| **Check pipeline** | `TRACK` anytime. |
| **System acting weird** | `DIAGNOSE` for full health check. |
| **Want autonomous mode** | `LIFTOFF` — I scan, synthesize, rank, present. You pick. |
| **Want background loop** | `DAEMON START` — hourly heartbeat, auto-cadence updates. |
| **Need to remember something** | `THOUGHT [topic]` — searches every session you've ever had. |

---

## THE PHILOSOPHER'S VIEW (Why This System Exists)

Office work is a game. Titles are costumes. Capabilities beat titles. Play well, collect cashflow, fund the life, break the cycle.

These tools do not add complexity. They REMOVE friction — the mechanical, repetitive 3D-avatar work of form-filling, clicking, copy-pasting. So YOU stay in the thinker's seat.

- **Decide** which company to target
- **Review** the output
- **Say YES or NO**

The machines do the typing. You do the thinking. That is the entire system.

---

*Last updated: 2026-06-24*
*Immutable. Always build on top.*
