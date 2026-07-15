# ABHIMANYU 2.0 — COMMANDS QUICK REFERENCE

## CORE LOOP

| Command | What It Does |
|---------|-------------|
| `FETCH` | Scan 41+ sources, return 24h-fresh jobs |
| `SHOOT [company]` | Write 16-section package |
| `YES` | Approve → auto-start networking timer |
| `AUTO-APPLY [company]` | Browser auto-submit |
| `AUTO-APPLY [company] --manual` | Phone blueprint |
| `TRACK` | Show pipeline kanban |

## DISCOVERY & INTELLIGENCE

| Command | What It Does |
|---------|-------------|
| `WIDENET` | Broadened FETCH |
| `SCAN` | **NEW** — Auto-scan 49 ATS providers via career-ops |
| `SCAN --company [name]` | Scan single company's ATS |
| `SCAN --verify` | Playwright-check URLs, drop expired |
| `SCAN --fresh` | Only 24h fresh results |
| `SCAN --dry-run` | Preview without writing files |
| `INTEL [company]` | **NEW** — Social intelligence on target company |
| `DOCTOR` | **NEW** — Check scanner/intelligence health |
| `ATOMIZE [paste JD]` | Extract company DNA |
| `SCORE [jd_text]` | TF-IDF fit score |
| `DISTILL [topic/url]` | Social intelligence harvest |
| `STATUS` | System health |
| `DIAGNOSE` | 10-phase diagnostics |
| `REFRESH` | Re-scan, replace stale |
| `AUDIT` | Full health audit |

## DOCUMENTS

| Command | What It Does |
|---------|-------------|
| `ALCHEMIZE [company]` | Gen resume + cover letter |
| `EVAL` | Score current resume against ops/consulting criteria |
| `EVAL --compare [v1] [v2]` | A/B test two resume versions |
| `EVAL --target [company]` | Evaluate alignment for specific company |
| `GENPDF [company]` | **NEW** — Generate ATS-optimized PDF resume (on-demand) |
| `GENPDF [company] --canva` | Generate via Canva design template |
| `OPTIMIZE LINKEDIN [company]` | Profile audit |
| `LINKEDIN APPLY-AUDIT` | Apply audit changes |

## LINKEDIN

| Command | What It Does |
|---------|-------------|
| `LINKEDIN CONNECT [name]` | Send connection request |
| `LINKEDIN INBOX` | Read messages |
| `LINKEDIN SEARCH [query]` | Search jobs |
| `CONTACT [name] [title] [company]` | Register contact |

## NETWORKING CADENCE

| Command | What It Does |
|---------|-------------|
| `CADENCE` | Full tracker |
| `CADENCE --footer` | Compact footer |
| `CADENCE --dashboard` | **Enhanced** — Show overdue/urgent/waiting/cold buckets |
| `CADENCE SUBMIT [company]` | Start T+0 timer |
| `CADENCE UPDATE [co] [leg] [action]` | Mark sent/replied/complete |
| `CADENCE CONTACT [co] [name] [title] [url]` | Add contact |
| `CADENCE DRAFT [company]` | **NEW** — Generate follow-up email/LinkedIn draft |
| `CADENCE RECORD [company]` | **NEW** — Record a follow-up you actually sent |
| `CADENCE PIN [co] [date]` | **NEW** — Pin specific next-follow-up date |

## LEARNING & PATTERNS

| Command | What It Does |
|---------|-------------|
| `LEARN [company] [outcome]` | Feed outcome back |
| `LEARN [company] --deep` | Full analysis + runs career-ops pattern analysis |
| `PATTERNS` | **NEW** — Run cross-application pattern analysis |
| `PATTERNS --quick` | Light check — pending outcomes only |
| `PATTERNS --min-threshold N` | Require min N entries per pattern |
| `THOUGHT [search]` | Search journal |
| `THOUGHT --today` | Today's log |
| `THOUGHT --last` | Last 10 prompts |

## OFFERS

| Command | What It Does |
|---------|-------------|
| `NEGOTIATE [company] [offer]` | Load negotiation playbook |

## AUTONOMOUS

| Command | What It Does |
|---------|-------------|
| `LIFTOFF` | Full autonomous cycle |
| `LIFTOFF --full` | Cycle + SHOOT + DEPLOY |
| `DAEMON START` | Background hourly loop |
| `DAEMON STOP` | Stop loop |
| `DAEMON STATUS` | Loop status |
| `DAEMON CONFIG` | Config |
| `INGEST [url]` | Feed social intel |
| `INGEST [url] --assimilate` | Queue assimilation |
| `INGEST --queue` | Pending assimilations |

## BATCH

| Command | What It Does |
|---------|-------------|
| `BATCH [co1, co2]` | Batch-approve Trust-tier |
| `BATCH --all` | Approve all Trust-tier |

## SYSTEM

| Command | What It Does |
|---------|-------------|
| `SYNC` | Sync AGENTS.md → all configs |
| `STATUS` | All skills health |
| `MANUAL-SUBMIT [company]` | Phone blueprint |
| `BROWSER [command]` | Direct browser commands |

## PIPELINE STATUS ICONS

| Icon | Meaning | Icon | Meaning |
|:----:|---------|:----:|---------|
| 🟢 | LIVE | 🔵 | SHOT |
| ✅ | SUBMITTED | 📞 | CALLBACK |
| 💰 | OFFER | ❌ | REJECTED |
| ⏸️ | PAUSED | 🟡 | SENT |
| 🔴 | OVERDUE | ⏳ | FUTURE |
| 🔍 | NEEDED | | |
