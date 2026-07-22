# ATS TECHNICAL SPECIFICATION MATRIX
## Per-Platform Parsing Rules: Format, Font, Spacing, Margins & File Type
## Cross-Reference Every Resume Against This Before Submission

---

### HOW TO USE
Before generating a resume for any company:
1. Identify their ATS (check job posting footer, career page URL, or 04_ATS_NUANCE_DB.md)
2. Look up that ATS in this file
3. Apply ALL technical specs for that platform
4. Run the verification checklist at the bottom

---

## PLATFORM TECHNICAL SPECS

### GREENHOUSE — Used by: EviSmart, Clio, Jobber, Wrapbook, Procurify

| Spec | Requirement |
|------|-------------|
| **File format** | DOCX preferred (parses more reliably); PDF acceptable if text-based single-column |
| **Font** | Arial, Calibri, Times New Roman, Georgia, Helvetica |
| **Font size** | Body: 10-12pt | Name: 14-16pt | Section headers: 11-13pt |
| **Line spacing** | 1.0-1.5 (single to 1.15 optimal) |
| **Margins** | 0.75" - 1" all sides |
| **Headers/footers** | AVOID — parser may skip contact info in headers. Place name/phone/email in body top 3 lines |
| **Date format** | "Month YYYY" or "MM/YYYY" — consistent throughout. "2017–2025" acceptable for ranges |
| **Section headers** | Use: Professional Summary, Professional Experience, Education, Core Competencies, Key Results |
| **Max pages** | 2 |
| **Max file size** | <500 KB |
| **Text** | Must be selectable (not image). Copy-paste must work cleanly |
| **Columns** | SINGLE COLUMN ONLY. Multi-column scrambles reading order |
| **Tables** | NEVER. Tables break parsing order |
| **Graphics/icons** | NEVER. Text in graphics is invisible to parser |
| **Bullets** | Standard • or - only. No special unicode, emoji, or decorative bullets |
| **PDF source** | Must be generated from Word/Google Docs (text-based), NOT from Canva/InDesign/Figma |
| **Keywords** | 2-4% keyword density. Place in context within bullets, not stuffed |
| **Scorecard** | Greenhouse does NOT auto-score. Human review with scorecard. Keywords still matter for search |
| **Parsing preview** | After upload, check that titles, dates, skills extracted correctly |

**Greenhouse-specific gotchas:**
- Text-as-image PDFs = completely invisible (parser sees zero text)
- Embedded fonts in PDF can cause rendering issues
- Contact info in first 3 lines is critical for parsing

---

### WORKDAY — Used by: lululemon, Telus, TELUS Digital, Arc'teryx

| Spec | Requirement |
|------|-------------|
| **File format** | DOCX strongly preferred (XML structure parses cleaner); PDF acceptable ONLY if text-based single-column |
| **Font** | Arial, Calibri, Times New Roman only |
| **Font size** | Body: 10-12pt | Name: 14-16pt | Section headers: 11-13pt |
| **Line spacing** | 1.0-1.15 |
| **Margins** | 0.75" - 1" all sides |
| **Headers/footers** | CRITICAL: Content in headers/footers may be SKIPPED entirely. Put ALL contact info in body |
| **Date format** | "Month YYYY" (e.g., "January 2017"). Must be CONSISTENT throughout. NOT "2017-2025" alone |
| **Section headers** | EXACT matches: "Professional Summary", "Professional Experience", "Education", "Skills", "Certifications". NOT creative alternatives |
| **Max pages** | 2 |
| **Max file size** | <1 MB (Workday handles up to 2MB but smaller is safer) |
| **Text** | Must be selectable text. Scanned images = empty profile |
| **Columns** | SINGLE COLUMN ONLY. Columns scramble job chronology |
| **Tables** | NEVER. Tables cause content to be read out of order |
| **Graphics/icons** | NEVER. Skill bars/progress charts = invisible |
| **Bullets** | Simple • or - only. Max 2-3 lines per bullet |
| **PDF source** | MUST be from Word/Google Docs. Canva/InDesign PDFs = vector paths = parser sees nothing |
| **Keywords** | Mirror JD phrasing exactly. Include BOTH acronym and full term: "CPA (Certified Public Accountant)" |
| **Skills section** | Weighted heavily. Include EVERY skill from JD. Concrete skills only (tools, certifications), not soft skills |
| **Form fields** | Workday requires manual form fields in addition to resume. Fill EVERY field. Don't leave blanks |
| **Job title match** | CRITICAL: Use their exact job title in your title field (e.g., "Director, Strategic Operations" not "COO") |

**Workday-specific gotchas:**
- Most parsing-failure-prone ATS for complex layouts
- "Illuminate" and "Skills Cloud" use semantic matching — skills in bullet context score higher than skills list alone
- Mixed date formats reduce timeline confidence (stick to one format)
- Large PDFs (>2MB) may be rejected entirely
- Some Workday instances accept only DOCX, rejecting PDFs

---

### LEVER — Used by: 1Password, TradeBeyond, Boomi

| Spec | Requirement |
|------|-------------|
| **File format** | PDF preferred; DOCX acceptable |
| **Font** | Arial, Calibri, Times New Roman |
| **Font size** | Body: 10-12pt | Name: 14-16pt |
| **Line spacing** | 1.0-1.5 |
| **Margins** | 0.75" - 1" all sides |
| **Headers/footers** | Avoid — same risk as other ATS |
| **Date format** | "Month YYYY" or "MM/YYYY" |
| **Section headers** | Standard: Summary, Experience, Education, Skills |
| **Max pages** | 2 (hard limit — Lever parsing degrades beyond 2) |
| **Max file size** | <500 KB |
| **Text** | Selectable text only |
| **Columns** | Single column |
| **Tables** | Never |
| **Graphics/icons** | Never |
| **Parsing style** | Less sophisticated than Greenhouse/Workday. Top-load keywords in first role |
| **Keywords** | First role description is most heavily parsed. Front-load strongest keywords there |

**Lever-specific gotchas:**
- Shorter resumes preferred (1.5-2 pages)
- Top portion (summary + first job) gets 70%+ of parsing weight
- Older/less relevant roles should be heavily summarized or cut
- Hyperlinks (LinkedIn URL) should be plain text, not embedded

---

### iCIMS — Used by: YVR, BDO, Vancouver Coastal Health

| Spec | Requirement |
|------|-------------|
| **File format** | PDF or DOCX both accepted. DOCX slightly safer |
| **Font** | Arial, Calibri, Times New Roman |
| **Font size** | Body: 10-12pt | Name: 14-16pt |
| **Line spacing** | 1.0-1.15 |
| **Margins** | 0.75" - 1" all sides |
| **Headers/footers** | Avoid — same risk |
| **Date format** | MUST include months: "January 2017 – March 2025". Year-only ranges may be misinterpreted |
| **Section headers** | Traditional only: Professional Summary, Professional Experience, Education, Skills |
| **Max pages** | 2 |
| **Max file size** | <500 KB |
| **Text** | Selectable text |
| **Columns** | Single column |
| **Tables** | Never |
| **Graphics/icons** | Never |
| **Title match** | Weights "Director" or "Manager" heavily. Ensure title includes target level |
| **Full company name** | Use full legal name, not abbreviations |
| **Industry** | Industry experience may be weighted (frame appropriately) |

**iCIMS-specific gotchas:**
- Classic/older parser — less forgiving of non-standard formatting
- Month-level dates required (not just years)
- Full company names improve parsing accuracy

---

### TALEO / Oracle Recruiting Cloud — Used by: Some large enterprises, government

| Spec | Requirement |
|------|-------------|
| **File format** | DOCX strongly preferred. PDF parsing is inconsistent and unreliable |
| **Font** | Arial, Calibri, Times New Roman — NO EXCEPTIONS |
| **Font size** | Body: 10-12pt | Name: 14-16pt |
| **Line spacing** | 1.0-1.5 |
| **Margins** | 0.75" - 1" all sides |
| **Headers/footers** | AVOID — content is invisible to Taleo parser |
| **Date format** | "Month YYYY" — MUST be identical format for every entry |
| **Section headers** | Standard only. Taleo fails to parse non-standard headers |
| **Max pages** | 2 (Taleo truncates at 2-3 pages) |
| **Max file size** | <500 KB |
| **Text** | Selectable text required |
| **Columns** | SINGLE COLUMN ONLY. Columns scramble content |
| **Tables** | NEVER — Taleo's older parser is the worst with tables |
| **Graphics/icons** | NEVER |
| **Special characters** | AVOID: emoji, unicode bullets, unusual symbols. Stick to ASCII: - or * |
| **Keywords** | Taleo uses aggressive keyword matching. Exact phrasing from JD required |
| **Profile fields** | Taleo often requires manual profile entry in addition to resume. Fill ALL fields thoroughly |
| **Copy-paste fields** | Many Taleo instances require pasting resume into text box. Have a clean plain-text version ready |
| **Text formatting** | Colored text/highlights stripped during parsing. Don't rely on color for meaning |

**Taleo-specific gotchas:**
- Oldest, most brittle parser — least forgiving of any formatting deviation
- PDFs from Canva/InDesign often parse as blank/empty
- Special characters frequently render as question marks or garbage
- Manual profile fields may be more important than uploaded resume for search ranking

---

### SMART RECRUITERS — Used by: Various mid-market tech companies

| Spec | Requirement |
|------|-------------|
| **File format** | DOCX preferred; PDF acceptable |
| **Font** | Arial, Calibri, Times New Roman, Georgia, Helvetica (99% recognition accuracy) |
| **Font size** | Body: 10-12pt | Headers: 14-16pt |
| **Line spacing** | 1.0-1.5 (over 2.0 causes section break confusion) |
| **Margins** | 0.5" minimum (below this may cut off text during parse) |
| **Headers/footers** | Avoid |
| **Date format** | "Month YYYY" |
| **Section headers** | Standard: Summary, Experience, Education, Skills |
| **Max pages** | 2 |
| **Max file size** | <500 KB |
| **Text** | Selectable text |
| **Columns** | Single column |
| **Tables** | Avoid |
| **Graphics/icons** | Avoid |

---

### BAMBOO HR — Used by: Smaller companies, mid-market

| Spec | Requirement |
|------|-------------|
| **File format** | PDF or DOCX |
| **Font** | Arial, Calibri, Times New Roman |
| **Font size** | Body: 10-12pt |
| **Line spacing** | 1.0-1.5 |
| **Margins** | 0.75" - 1" |
| **Headers/footers** | Avoid |
| **Date format** | "Month YYYY" |
| **Section headers** | Standard |
| **Max pages** | 2 |
| **Columns** | Single column |
| **Tables/Graphics** | Avoid |

**BambooHR-specific:**
- Less sophisticated parser — simpler resumes parse better
- Clear section headers critical

---

### JAZZ HR — Used by: SMBs, mid-market

| Spec | Requirement |
|------|-------------|
| **File format** | PDF or DOCX |
| **Font** | Arial, Calibri, Times New Roman |
| **Font size** | Body: 10-12pt |
| **Line spacing** | 1.0-1.5 |
| **Margins** | 0.75" - 1" |
| **Headers/footers** | Avoid |
| **Date format** | "Month YYYY" |
| **Section headers** | Standard |
| **Max pages** | 2 |
| **Columns** | Single column |
| **Tables/Graphics** | Avoid |

**JazzHR-specific:**
- Simple format, clear skills section = best results
- Skills section heavily weighted

---

### SUCCESSFACTORS (SAP) — Used by: Large enterprises

| Spec | Requirement |
|------|-------------|
| **File format** | DOCX preferred |
| **Font** | Arial, Calibri, Times New Roman |
| **Font size** | Body: 10-12pt |
| **Line spacing** | 1.0-1.5 |
| **Margins** | 0.75" - 1" |
| **Headers/footers** | Avoid |
| **Date format** | "Month YYYY" |
| **Section headers** | Standard |
| **Max pages** | 2 |
| **Columns** | Single column |
| **Tables/Graphics** | Avoid |

**SuccessFactors-specific:**
- Enterprise fields require consistency (education, certifications, etc.)
- Profile data may be more important than resume text for matching

---

## GLOBAL ATS RULES (Apply to ALL Platforms)

| Rule | Details |
|------|---------|
| **File format** | DOCX is safest across ALL platforms. PDF (text-based) is acceptable for Greenhouse, Lever, iCIMS. Avoid PDF for Workday, Taleo |
| **Font** | Arial or Calibri only (both render perfectly on ALL systems) |
| **Font size** | 11pt body text — universally compatible. 10pt is too small for older parsers. 12pt is fine but reduces content per page |
| **Margins** | 0.75" minimum on all sides. 0.5" is risk of text cutoff |
| **Line spacing** | 1.0-1.15 — single space with small paragraph gap |
| **Bullets** | Standard • or - only. Never use: → ⇒ ➢ ✦ ◆ ✓ ☐ ▶ ◆ |
| **Date format** | "Month YYYY" (e.g., "January 2017") — accepted by ALL ATS. Never use relative dates ("Present" is fine) |
| **Section headers** | Professional Summary, Professional Experience, Education, Core Competencies, Key Results — these are universal |
| **Columns** | NEVER use columns for ANY ATS |
| **Tables** | NEVER use tables for ANY ATS |
| **Graphics** | NEVER use graphics, logos, icons, charts for ANY ATS |
| **Headers/footers** | NEVER put content in headers/footers. All critical info in body |
| **Name** | First line of document, bold, 14-16pt. "Name: Aryan S." format helps Workday parsing |
| **Contact** | Lines 2-3: Phone, Email, LinkedIn, Location — all in plain text |
| **LinkedIn URL** | Plain text URL (e.g., linkedin.com/in/aryan). NOT hyperlinked text |
| **PDF generation** | Always from Word/Google Docs → Export as PDF. Never from Canva/InDesign/Figma/Photoshop |
| **File name** | `CompanyName_RoleTitle_ARYAN_RESUME.pdf` — no generic names |
| **Metadata** | Strip author name, company name from file properties |

---

## COMPANY → ATS CROSS-REFERENCE

| Company | ATS | File Format to Use | Key Risk |
|---------|-----|-------------------|----------|
| EviSmart | Greenhouse | DOCX (or PDF) | Text-as-image PDFs |
| Clio | Greenhouse | DOCX | Multi-column layouts |
| Jobber | Greenhouse | DOCX | Headers/footers |
| Wrapbook | Greenhouse | DOCX | Embedded fonts |
| Procurify | Greenhouse | DOCX | Non-standard bullets |
| lululemon | Workday | DOCX ONLY | Headers/footers skip; date format |
| Telus | Workday | DOCX ONLY | Title mismatch; form fields left blank |
| TELUS Digital | Workday | DOCX ONLY | Skills Cloud mismatch |
| Arc'teryx | Workday | DOCX ONLY | Non-standard section headers |
| 1Password | Lever | PDF | Resume beyond 2 pages |
| YVR | iCIMS | DOCX | Month-level dates missing |
| BDO | iCIMS | DOCX | Year-only dates |
| VCH | iCIMS | DOCX | Company name abbreviation |

---

## PRE-SUBMISSION VERIFICATION CHECKLIST

Run this for EVERY application before hitting submit:

### File Format & Technical
- [ ] File saved as DOCX (preferred) or text-based PDF
- [ ] File size <500 KB (PDF) or <1 MB (DOCX)
- [ ] Text is selectable (copy-paste test passed)
- [ ] File name: `Company_Role_ARYAN_RESUME.pdf`
- [ ] Metadata stripped (no author, no company name in properties)

### Layout & Formatting
- [ ] Single-column layout
- [ ] No tables, columns, text boxes, graphics, icons
- [ ] No content in headers or footers
- [ ] Contact info in body top 3 lines
- [ ] Name on line 1 (bold, 14-16pt)
- [ ] Font: Arial or Calibri only (11pt body)
- [ ] Margins: 0.75" minimum all sides
- [ ] Line spacing: 1.0-1.15
- [ ] Max 2 pages

### Content
- [ ] Standard section headers used (Summary, Experience, Education, Skills)
- [ ] Date format consistent throughout (Month YYYY)
- [ ] No special unicode characters, emoji, or decorative bullets
- [ ] Keywords from JD embedded in context (not stuffed)
- [ ] Job title matches target role title
- [ ] LinkedIn URL as plain text
- [ ] Bullets use simple • or - only

### ATS-Specific
- [ ] Platform-specific rules applied (from table above)
- [ ] Parsing preview checked (if available after upload)
- [ ] Form fields filled (Workday/Taleo)
- [ ] Plain text version ready (Taleo copy-paste fields)
