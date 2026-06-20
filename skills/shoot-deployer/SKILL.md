---
name: shoot-deployer
description: "Triggered when user says SHOOT, SHOOT [company name], or pastes a JD for the 15-section master output (upgraded from 13 — added Company Scout + Hiring Process Reveal). Generates the complete 15-section application package for proofreading. Every section shown in chat before any file touches disk. Never shortcut, never streamline — full depth every time."
---

# SHOOT DEPLOYER — Full 13-Section Application Package

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

## The 15 Sections (Every Job, Every Time)

### 1. HEADER
Company, Role, Team, Salary (range + midpoint), Location, Fit Score, Pipe, Wave, NOC, TEER, Archetype

**Pipe positioning pre-selected:** Run the decision tree from POSITIONING BY PIPE FRAMEWORK in AGENTS.md. Read company DNA → select pipe frame → blend if needed → choose archetype. All 15 sections flow from this selection.

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

### 4. CORE Alignment Matrix
One-liner + Table: `JD Requirement → Aman's Map` (what they need → what he's done)

### 3. DNA EXTRACTION
- Company background + market position
- Language Registry (exact words they use — these go into resume at 2-4% density)
- Value System (what they reward)
- Cultural Cues (how they communicate)
- Anti-Patterns (what they hate — never include these)

### 4. ATS SPECS
- Platform (Greenhouse/Workday/Lever/Ashby/etc.)
- Font, Size, Format, Margins, Section Headers, Special Rules
- DOCX per spec, 100% parseable

### 5. DEVICE MAP
- Hardware they issue, OS, peripherals, IT policy, Day 1 prep

### 6. RESUME TEXT (Plain)
- Tailscale style: Name+contact centered, Professional Summary (3-4 sentences), Core Competencies (pipe-separated), Experience (Company — Title | Location, metrics bullets), Education, Technical Proficiency
- LOCAL CANADIAN IN BC framing — no immigration language
- In code fence for proofreading

### 7. RESUME LATEX (.tex source)
- Full LaTeX source with proper formatting
- `\textbf{Company} \hfill \textbf{Title}` pattern
- `\begin{itemize}` for bullets
- Liberation Sans 10pt

### 8. COVER LETTER TEXT (Plain)
- 6-paragraph narrative mirroring company DNA
- Header: `[NAME]` / Date: DD/MM/YYYY / Vancouver, BC, Canada
- Closing: Best regards, `[NAME]` / Phone: `[PHONE]` / Email: `[EMAIL]` / LinkedIn: `[LINKEDIN]`
- In code fence for proofreading

### 9. COVER LETTER LATEX (.tex source)
- Full LaTeX with mailto + https hyperlinks

### 10. LINKEDIN OUTREACH (4-Tier)
- T+0: Connect + note to IC/Associate
- T+3: Follow-up to Manager/Director
- T+7: Value-add to Sr IC/Manager
- T+14: Final nudge to Exec Sponsor
- Each with full message text + persona rationale

### 11. INTERVIEW CHEAT SHEET
- 60-sec pitch
- 5 Q&A with specific answers (not generic)
- 3 STAR stories (Profitability, Credibility, Visibility pillars)
- Keywords to use, anti-patterns to avoid
- "One year from now" question
- Rejection response script

### 14. CHECKLIST (17+ Items)
- DNA extracted? ATS keywords at 2-4%? Title aligned? No immigration language? DOCX ready? etc.
- Company scout completed? Hiring process revealed? Provenance verified?

### 15. FOLLOW-UP + FINOPS
- T+0 through T+28 cadence with conditional triggers
- FinOps: negotiation targets, walk-away floor, benefits leverage

## Proofreading Protocol
1. SHOW full 15-section in chat (upgraded from 13 — Company Scout + Hiring Process Reveal are new)
2. User proofreads
3. User says "looks good" / "proceed" / "save it" / "approved" → only THEN save files
4. Write DOCX via document-engine
5. Git commit + push
6. Advance to next job
