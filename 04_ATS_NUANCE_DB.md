# ATS NUANCE DATABASE
## Per-Company Parsing Rules & Optimization

---

### GREENHOUSE (Used by: Clio, Jobber, EviSmart, Procurify)

**Parser Behavior:**
- Text-only parsing. Ignores tables, columns, graphics, images
- Reads top-to-bottom, left-to-right
- Scores on keyword density (2-4% optimal)
- Rejects PDFs with text-as-image (must be selectable text)

**Optimization Rules:**
- ✅ Single-column layout
- ✅ Standard section headers: "Experience", "Education", "Skills"
- ✅ Keywords from JD placed in context (not stuffed)
- ❌ No tables, columns, graphics, icons
- ❌ No headers/footers with text
- ❌ No text boxes or floating elements
- ❌ No PDF with embedded fonts (use standard fonts)

**Resume Format:**
```
[NAME]
[Contact]

PROFESSIONAL SUMMARY
[3-4 lines, includes top 3 JD keywords]

PROFESSIONAL EXPERIENCE
[Company], [Title]
[dates]
• [bullet with keyword]
• [bullet with keyword]

EDUCATION
[School], [Degree]

CORE COMPETENCIES
[keyword], [keyword], [keyword]
```

---

### WORKDAY (Used by: Telus, EY, Aritzia, Vancouver Coastal Health)

**Parser Behavior:**
- Heavy keyword matching — scans for exact JD phrase matches
- Title match is critical (must match their job title exactly or close)
- Skills section heavily weighted
- Location, education, years of experience all auto-extracted
- Requires manual form fields in addition to resume upload

**Optimization Rules:**
- ✅ Include ALL synonyms for JD skills
- ✅ Match your "Job Title" field to their listed title (use "Director, Strategic Operations" not "COO")
- ✅ In Skills section, include every skill mentioned in JD
- ✅ Years of experience: round up conservatively
- ✅ Education: list every degree, diploma, certificate
- ❌ Don't leave any form field blank
- ❌ Don't exaggerate years beyond believability

**Resume Format:**
```
[NAME]
[Contact]

WORK EXPERIENCE
[Title that matches target title]
[Company]
[dates]
[Description with JD keyword phrases included verbatim where natural]

SKILLS
[JD Skill 1], [JD Skill 2], [JD Skill 3]...
[Include ALL skills from JD]

EDUCATION
...

CERTIFICATIONS
...
```

---

### LEVER (Used by: TradeBeyond, Boomi)

**Parser Behavior:**
- Short-form preferred (2 pages max)
- Parses top portion heavily (summary and first job)
- PDF upload with basic text extraction
- Less sophisticated than Greenhouse/Workday

**Optimization Rules:**
- ✅ Lead with strongest, most relevant experience
- ✅ Cut older/less relevant roles
- ✅ 2 pages absolute maximum
- ✅ Front-load keywords in first role description

**Resume Format:**
```
[NAME] — [Target Title]
[Contact]

SUMMARY
[3 lines, value proposition for THIS company]

CURRENT/PREVIOUS ROLE
[Most relevant role — full description]
• [Keyword-heavy bullets]

OTHER EXPERIENCE
[2nd role — shorter]
[3rd role — 1-2 bullets max]

EDUCATION
...
```

---

### iCIMS (Used by: BDO, Vancouver Coastal Health, YVR)

**Parser Behavior:**
- Classic PDF parser
- Reads sequential text
- Weights "Manager" or "Director" title match heavily
- Industry experience weighted (healthcare → health authority roles = bonus, but can be framed)

**Optimization Rules:**
- ✅ Traditional resume format
- ✅ Include months in dates (e.g., "Jan 2017 - Mar 2025")
- ✅ Use full company name
- ✅ Standard fonts (Arial, Calibri, Times New Roman)
- ❌ No creative formatting
- ❌ No columns

**Resume Format:**
```
[NAME]
[Address] | [Phone] | [Email]

PROFESSIONAL SUMMARY
[3-4 lines]

PROFESSIONAL EXPERIENCE

[Company Name], [City, Province]
[Title] | [Month Year] - [Month Year]
[Description paragraph + bullets]

EDUCATION
...
```

---

### UNKNOWN/CUSTOM ATS (All other companies)

**Safety Rules:**
1. Default to Greenhouse format (most restrictive)
2. No columns, tables, graphics
3. Single-column, text-only
4. Standard section headers
5. Keywords from JD in context
6. Machine-readable PDF (selectable text)
7. 2 pages max
