# HARD KERNEL RULE – UNIVERSAL CADENCE (IMMUTABLE CORE)

**Goal** – Provide a single, immutable workflow that applies to *every* job application, regardless of company, role, or pipeline. The rule defines the **core cadence** that must always occur, while allowing **company‑specific optional legs** (e.g., extra assessments, coding tests) to be injected without breaking the core.

---

## 1️⃣ Core Cadence (must execute in order)
| Step | Description | Trigger | System command (auto‑generated) |
|------|-------------|---------|--------------------------------|
| **0 – Referral / Endorsement** | Candidate provides a referral brief or endorsement PDF to a trusted contact (Kash, recruiter, internal champion). | Candidate sends email/WhatsApp/Slack with PDF. | `CADENCE UPDATE [company] Leg 0` (marks ✅). |
| **1 – Application Submission** | Candidate submits PDF (or web form) via the company portal. | Portal returns an acknowledgment email or status page. | `CADENCE UPDATE [company] Leg 1` → PIPELINE status **✅ SUBMITTED**. |
| **2 – Hiring‑Manager Discovery** | Trusted contact (or recruiter) supplies the hiring‑manager’s name and contact method. | Email/WhatsApp reply. | `CADENCE UPDATE [company] Leg 2`. |
| **3 – LinkedIn Connection** | Candidate sends a LinkedIn connection request to the hiring‑manager (or senior stakeholder). | Connection request accepted. | `CADENCE UPDATE [company] Leg 3`. |
| **4 – Value‑Add Outreach** | Candidate emails a concise insight (e.g., industry trend, product idea) that embeds **360° intelligence** (live company news, funding, recent launches). | Email sent. | `CADENCE UPDATE [company] Leg 4`. |
| **5 – Final Nudge** | If no response after 7 days, send a short follow‑up reminder. | Follow‑up sent. | `CADENCE UPDATE [company] Leg 5`. |
| **6 – Phone‑Screen** | Recruiter schedules a 15‑30 min phone interview. | Call completed. | `INTERVIEW‑PREP [company]`; then `TRACK --add [company] PHONE_SCREEN_DONE`. |
| **7 – Case‑Study (optional)** | Some companies request a take‑home case. | Candidate submits PDF. | `INTERVIEW‑PREP [company] CASE`; then `TRACK --add [company] CASE_STUDY_DONE`. |
| **8 – Panel / Virtual Interview** | 2‑3 hour interview with multiple stakeholders. | Interview finished. | `INTERVIEW‑PREP [company] PANEL`; then `TRACK --add [company] PANEL_DONE`. |
| **9 – Offer Generation** | Recruiter sends formal offer (salary, equity, bonuses). | Offer email received. | `NEGOTIATE [company] "<offer‑details>"` → prints net‑per‑fortnight and stores `salary_breakdown.md`. |
| **10 – Offer Acceptance** | Candidate signs and returns the offer letter. | Acceptance email/DocuSign completed. | `CADENCE UPDATE [company] OfferAccepted`; `TRACK --add [company] STARTED`. |
| **11 – On‑boarding** | HR sends benefits, tax forms, and device/WFH preferences. | All forms completed. | `TRACK --add [company] ONBOARDING_DONE`. |
| **12 – First Paycheck** | Payroll processes the first bi‑weekly payment. | Paycheck deposited. | `THOUGHT LOG "<date> – First paycheck of $<net> received."`; `TRACK --add [company] FIRST_PAYCHECK`. |

**Note:** Steps 7 (Case‑Study) and any additional assessments are **optional** and can be inserted after Step 6 or before Step 9. The core steps (0‑6, 8‑12) are immutable and must appear in this order.

---

## 2️⃣ 360° INTELLIGENCE (DNA‑1) – Always present
- Nightly `LIFTOFF` agent scrapes: company website, news releases, Glassdoor/Indeed reviews, LinkedIn updates, Crunchbase/PitchBook funding, X.com/Reddit chatter, and JD‑derived keywords via `ATOMIZE`.
- Results stored in `data/intel/[company]/` and `data/dna/[company]/role_dna.md`.
- Every cadence email/template pulls **the latest two‑sentence snippet** automatically (system‑generated placeholder `{{intel_snippet}}`).

---

## 3️⃣ SALARY BREAK‑DOWN (ENFORCED)
1. Gross per fortnight = `annual_base / 26`.
2. Approx. 32 % total deductions (federal ~22 %, BC ~9 %, CPP 5.95 % up to max, EI 1.63 % up to max).
3. Net per fortnight = `gross * 0.68` (rounded).
4. After `NEGOTIATE`, the system prints and saves the breakdown in `data/negotiation/[company]/salary_breakdown.md` and appends the line to the cadence footer. Missing breakdown → pipeline flagged `❗ SALARY BREAKDOWN MISSING`.

---

## 4️⃣ WORK‑FROM‑HOME & DEVICE POLICY (ENFORCED)
- **Default:** Full remote unless JD explicitly requires on‑site.
- **Device hierarchy:**
  1. Desktop/Laptop (Ubuntu/Linux) – primary.
  2. Phone/Termux – automatic fallback (`PHONE_MODE=true`) when desktop tools (Chrome, Playwright) are unavailable.
- When falling back, the system generates a **MANUAL‑SUBMIT** blueprint (`data/networking/[company]/manual_submit.md`). The cadence footer always displays the current mode (`Desktop` vs `Phone`).
- On‑boarding prompts for WFH preference and stores it in `data/onboarding/[company]/preferences.md`.

---

## 5️⃣ HARD ENFORCEMENTS (must never be bypassed)
1. **EVAL PASS** – `EVAL` must return **PASS ≥ 70** before any DOCX/PDF is written. Failure → pipeline set to `❌ BLOCKED` and automatic resume rewrite is triggered.
2. **Dual‑Write** – Every generated DOCX/PDF must exist **both** in the Linux worktree (`ABHIMANYU‑2.0/YYYY‑MM‑DD/[company]/`) **and** in OneDrive (`/mnt/c/Users/owner/OneDrive/ABHIMANYU‑2.0/...`). Missing file aborts the step.
3. **Thought‑Journal** – Every state‑changing command appends a line to `data/thought_log/YYYY‑MM‑DD.md` (ISO timestamp + brief description). Absence → pipeline error.
4. **Cadence Footer** – After any pipeline or cadence update, `CADENCE_FOOTER.md` is regenerated and **appended** to **every** system response (including plain‑text). Missing footer → `⚠️ Cadence footer missing` error.
5. **Auto‑Push** – After each command that changes state, the system runs `git add -A && git commit -m "[action] — [company] — <timestamp>" && git push`. Failure on second attempt aborts the operation.
6. **Device‑Mode Validation** – If a step requires a desktop tool and `PHONE_MODE=true`, the system automatically switches to `MANUAL‑SUBMIT` mode and logs the change.
7. **Salary‑Break‑down Presence** – After `NEGOTIATE` the net‑per‑fortnight line must exist; otherwise pipeline is flagged `❗ SALARY BREAKDOWN MISSING`.

---

## 6️⃣ EXAMPLE FLOW (Seaspan – using the universal core)
1. **Leg 0** – Referral PDF sent to Kash (`CADENCE UPDATE Leg 0`).
2. **Leg 1** – Portal auto‑email confirms receipt (`CADENCE UPDATE Leg 1`).
3. **Leg 2** – Kash replies with hiring‑manager name (`CADENCE UPDATE Leg 2`).
4. **Leg 3** – LinkedIn request to hiring‑manager, pulling live‑intel snippet (`CADENCE UPDATE Leg 3`).
5. **Leg 4** – Value‑add email referencing recent Oracle‑Cloud rollout (`CADENCE UPDATE Leg 4`).
6. **Leg 5** – Final nudge if no reply (`CADENCE UPDATE Leg 5`).
7. **Phone‑Screen** – `INTERVIEW‑PREP Seaspan`; after call `TRACK --add Seaspan PHONE_SCREEN_DONE`.
8. **Case‑Study** – (optional) `INTERVIEW‑PREP Seaspan CASE`; submit → `TRACK --add CASE_STUDY_DONE`.
9. **Panel** – `INTERVIEW‑PREP Seaspan PANEL`; after interview `TRACK --add PANEL_DONE`.
10. **Offer** – `NEGOTIATE Seaspan "base=$138k, equity=0.18%, signing=$7k"` → prints net $3,610 per fortnight.
11. **Acceptance** – `CADENCE UPDATE OfferAccepted`; `TRACK --add STARTED`.
12. **On‑boarding** – Remote preference captured, device checklist generated.
13. **First Paycheck** – Net $3,610 deposited; `THOUGHT LOG` and `TRACK --add FIRST_PAYCHECK` complete the loop.

---

## 7️⃣ QUICK COMMAND CHEAT‑SHEET (copy‑paste)
```bash
# Core steps (run in order)
CADENCE UPDATE [company] Leg 0   # referral sent
CADENCE UPDATE [company] Leg 1   # portal submitted
# wait for hiring‑manager name → then:
CADENCE UPDATE [company] Leg 2
CADENCE UPDATE [company] Leg 3   # LinkedIn connect
CADENCE UPDATE [company] Leg 4   # value‑add email
CADENCE UPDATE [company] Leg 5   # final nudge (if needed)

# Phone screen
INTERVIEW-PREP [company]
TRACK --add [company] PHONE_SCREEN_DONE

# Optional case study
INTERVIEW-PREP [company] CASE
TRACK --add [company] CASE_STUDY_DONE

# Panel interview
INTERVIEW-PREP [company] PANEL
TRACK --add [company] PANEL_DONE

# Offer negotiation (replace numbers as needed)
NEGOTIATE [company] "base=$138k, equity=0.18%, signing=$7k"

# Acceptance & onboarding
CADENCE UPDATE [company] OfferAccepted
TRACK --add [company] STARTED

# First paycheck (log manually if needed)
THOUGHT LOG "2026-08-19 – First paycheck of $3,610 net received."
TRACK --add [company] FIRST_PAYCHECK
```
All commands automatically update the pipeline, cadence footer, thought journal, and push to GitHub.

---

*This rule is **immutable** and will be enforced for **every future job‑application cadence**, ensuring that the core steps (Referral → First Paycheck) are always executed in the correct order, with 360° intelligence, salary transparency, and WFH/device awareness woven in.*