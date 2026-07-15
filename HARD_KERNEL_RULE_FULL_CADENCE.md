# HARD KERNEL RULE – FULL CADENCE & COMPENSATION

Purpose:
- Immutable workflow for every job application (SHOOT or LIFTOFF) from resume generation to first paycheck.
- 360° intelligence (company news, reviews, LinkedIn, funding, social) is woven into each touchpoint.
- Salary breakdown per fortnight (gross → net) and WFH/device policy are enforced.

Scope:
- Applies to all companies in TICS pipelines (data/pipeline/PIPELINE.md).
- Excludes roles that fail hard filters (credit‑check risk, heavy‑Excel/Quant, finance domain).
- Hard rule cannot be overridden without admin approval.

360° Intelligence (DNA‑1):
- Sources: company site, Glassdoor/Indeed, LinkedIn, Crunchbase/PitchBook, X.com/Reddit, JD analysis (ATOMIZE).
- Nightly LIFTOFF agent writes files under data/intel/[company]/ and data/dna/[company]/role_dna.md.
- Cadence messages automatically include the latest snippet (max 2 sentences).

Cadence Structure (Leg 0 → Paycheck):
- Leg 0 – Referral/endorsement: send PDF to trusted contact (Kash). -> `CADENCE UPDATE Leg 0`.
- Leg 1 – Application submission: portal auto‑email confirms receipt. -> PIPELINE status ✅ SUBMITTED, `CADENCE UPDATE Leg 1`.
- Leg 2 – Hiring‑manager name: trusted contact replies. -> `CADENCE UPDATE Leg 2`.
- Leg 3 – LinkedIn connection: send request using live‑intel snippet. -> `CADENCE UPDATE Leg 3`.
- Leg 4 – Value‑add outreach: email concise insight using company KPI from DNA‑1. -> `CADENCE UPDATE Leg 4`.
- Leg 5 – Final nudge: follow‑up if no reply after 7 days. -> `CADENCE UPDATE Leg 5`.
- Phone‑screen: run `INTERVIEW-PREP`, then `TRACK --add [company] PHONE_SCREEN_DONE`.
- Case study (optional): `INTERVIEW-PREP CASE`, submit PDF, `TRACK --add CASE_STUDY_DONE`.
- Panel interview: `INTERVIEW-PREP PANEL`, `TRACK --add PANEL_DONE`.
- Offer: run `NEGOTIATE` with base, equity, signing. System prints net per fortnight.
- Acceptance: `CADENCE UPDATE OfferAccepted`, `TRACK --add STARTED`.
- First paycheck: verify net matches salary‑breakdown, log THOUGHT, `TRACK --add FIRST_PAYCHECK`.

Salary Breakdown Rule:
- Gross per fortnight = annual_base / 26.
- Approx. 32% total deductions (federal ~22%, BC ~9%, CPP 5.95% up to max, EI 1.63% up to max).
- Net per fortnight = gross * 0.68 (rounded).
- Equity and signing bonus are tracked separately, not in net cash.
- After `NEGOTIATE` the breakdown is printed and saved to `data/negotiation/[company]/salary_breakdown.md` and appended to the cadence footer.

WFH & Device Policy:
- Default remote unless JD requires on‑site.
- Primary device: desktop/linux. If `google-chrome` missing, auto‑switch to PHONE_MODE and generate MANUAL‑SUBMIT blueprint (saved under `data/networking/[company]/manual_submit.md`).
- Cadence footer always shows current device mode.
- On‑boarding prompts for WFH preference and device; stores in `data/onboarding/[company]/preferences.md` and creates device‑specific checklist.

Hard Enforcements (must never be bypassed):
1. EVAL must PASS (score ≥70) before any DOCX/PDF is saved.
2. Dual‑write: every generated DOCX/PDF must exist in both Linux worktree and OneDrive.
3. Thought‑journal entry required for every state‑changing command.
4. Cadence footer regenerated and appended to every system response.
5. After each command the system runs `git add -A && git commit -m "[action] — [company] — <timestamp>" && git push`; abort on second failure.
6. Device‑mode validation forces MANUAL‑SUBMIT when desktop tools unavailable.
7. Salary‑breakdown line must be present after offer; missing triggers ❗ SALARY BREAKDOWN MISSING error.

Example (Seaspan):
Day0 referral sent -> `CADENCE UPDATE Leg0`.
Day1 portal confirms -> PIPELINE ✅ SUBMITTED.
Day2 Kash returns hiring‑manager -> `CADENCE UPDATE Leg2`.
Day3 LinkedIn connect (uses live‑intel snippet) -> `CADENCE UPDATE Leg3`.
Day5 value‑add email -> `CADENCE UPDATE Leg4`.
Day7 final nudge -> `CADENCE UPDATE Leg5`.
Day12 phone‑screen: `INTERVIEW-PREP`, then `TRACK --add PHONE_SCREEN_DONE`.
Day15 case study: `INTERVIEW-PREP CASE`, `TRACK --add CASE_STUDY_DONE`.
Day22 panel: `INTERVIEW-PREP PANEL`, `TRACK --add PANEL_DONE`.
Day24 offer (base $138k, equity 0.18%, signing $7k) -> `NEGOTIATE`; prints net $3,610 per fortnight.
Day26 acceptance -> `CADENCE UPDATE OfferAccepted`.
Day27 onboarding remote, laptop device stored.
Day31 start date recorded.
Day45 first paycheck lands, net $3,610 + prorated signing; THOUGHT logged, `TRACK --add FIRST_PAYCHECK`.

Quick command cheat‑sheet:
```bash
CADENCE UPDATE [company] Leg <0-5>
INTERVIEW-PREP [company]
INTERVIEW-PREP [company] CASE
INTERVIEW-PREP [company] PANEL
NEGOTIATE [company] "base=$138k, equity=0.18%, signing=$7k"
THOUGHT LOG "2026-08-19 – First paycheck of $3,610 net received."
TRACK --add [company] STARTED
TRACK --add [company] FIRST_PAYCHECK
```
All updates auto‑push to GitHub per the global push rule.