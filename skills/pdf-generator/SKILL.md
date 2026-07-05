---
name: pdf-generator
version: "1.0.0"
description: >
  On-demand ATS-optimized PDF resume generation using career-ops engine.
  Only runs when user explicitly asks with GENPDF command.
  DOCX remains the default format — PDF is optional.
triggers:
  - command: GENPDF [company]
    description: "Generate ATS-optimized PDF resume for a company"
    options:
      - "--cv" : Use cv.md from project root
      - "--ats" : Generate ATS-optimized HTML+PDF
      - "--canva" : Launch Canva design (if Canva ID configured)
  - command: GENPDF [company] --ats
    description: "Generate ATS-optimized PDF with keyword injection"
---

# PDF GENERATOR SKILL — career-ops PDF Adapter

## Location
PDF script: `lib/career-ops/generate-pdf.mjs`
Template: `lib/career-ops/templates/cv-template.html`
Fonts: `lib/career-ops/fonts/`
Profile: `lib/career-ops/config/profile.yml`

## Prerequisites
- Playwright Chromium installed (required for HTML→PDF rendering)
  ```bash
  npx playwright install chromium
  ```
- cv.md source of truth at project root

## On-Demand Only — Never Auto-Generates

GENPDF runs ONLY when you type `GENPDF [company]`. It does NOT auto-run on FETCH, SHOOT, or any other command.

## Command

### GENPDF [company]

```bash
# 1. Read JD context (from SHOOT package or user paste)
# 2. Extract 15-20 keywords from JD
# 3. Build recruiter risk map (what doubts will recruiter have?)
# 4. Rewrite Professional Summary with JD keywords
# 5. Reorder experience bullets by JD relevance + risk map
# 6. Generate HTML from cv-template.html
# 7. Generate PDF:
node lib/career-ops/generate-pdf.mjs output/cv-{candidate}-{company}.html output/cv-{candidate}-{company}-{YYYY-MM-DD}.pdf --format=letter
```

**Output fields:** PDF path, page count, keyword coverage %

### GENPDF [company] --canva

If Canva resume design ID is configured in `config/profile.yml`, generate via Canva API instead.

## ATS Rules (applied to every PDF)
- Single-column layout (no sidebars)
- Standard section headers
- No text in images/SVGs
- UTF-8, selectable text (not rasterized)
- Distributed JD keywords: Summary + first bullet of each role + Skills
- No hidden text, no keyword stuffing, no white-font tricks

## Design
- **Fonts:** Space Grotesk (headings) + DM Sans (body)
- **Margins:** 0.6in
- **Background:** Pure white
- **Recruiter 6-second scan:** top third must make target role + strongest fit + proof obvious
