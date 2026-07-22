#!/usr/bin/env python3
"""
FETCH ENGINE v2 — JOBS OS 2026
Hybrid Architecture: Auto-fetch (Greenhouse) + URL generation (HiringCafe + LinkedIn + Career pages)

SOURCE STACK:
  Tier 1 — Auto-fetch: Greenhouse API (5 working boards: Brex, Hootsuite, EviSmart, Thinkific, Practice Better)
  Tier 2 — Manual browser: HiringCafe (primary discovery via generated search URLs)
  Tier 3 — Cross-check: LinkedIn Jobs (verify shortlisted roles)
  Tier 4 — Career pages: Direct links to target company career sites

Usage:
  python3 33_FETCH_ENGINE.py              # Full fetch: auto-fetch Greenhouse + generate all URLs
  python3 33_FETCH_ENGINE.py --fetch      # Auto-fetch only (Greenhouse)
  python3 33_FETCH_ENGINE.py --urls       # Generate search URLs only (for manual browsing)
  python3 33_FETCH_ENGINE.py --pipe SaaS  # Single pipe
  python3 33_FETCH_ENGINE.py --score      # Score a pasted JD
"""

import requests
import re
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────

SYSTEM_ROOT = Path("/home/aryan/opencode_test/JOBS-OS-2026")
CORPUS_FILE = SYSTEM_ROOT / "01_MASTER_CORPUS.md"
TRACKING_FILE = SYSTEM_ROOT / "TRACKING.md"
OUTPUT_FILE = SYSTEM_ROOT / "07_21_JOBS_FIT_ASSESSMENT.md"
PACKAGES_DIR = SYSTEM_ROOT / "APPLICATION_PACKAGES"
JOBS_DB = SYSTEM_ROOT / "data" / "jobs.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

TIMEOUT = 15
MIN_PER_PIPE = 5
MAX_PER_PIPE = 10

# ──────────────────────────────────────────────
# WORKING GREENHOUSE BOARDS (verified accessible)
# ──────────────────────────────────────────────

GREENHOUSE_BOARDS = {
    "Brex": "brex",
    "Hootsuite": "hootsuite",
    "EviSmart": "evismart",
    "Thinkific": "thinkific",
    "Practice Better": "practicebetter",
}

# ──────────────────────────────────────────────
# 5-PIPE ARCHITECTURE
# ──────────────────────────────────────────────

PIPES = {
    "Corporate": {
        "label": "🏢 CORPORATE",
        "description": "Canadian corps, banks, telco, crown corps, retail, insurance",
        "hiring_cafe_queries": [
            "director+operations+Vancouver+Canada",
            "director+strategy+Vancouver+Canada",
            "director+business+operations+Canada+remote",
            "senior+manager+operations+Vancouver+Canada",
            "chief+of+staff+Vancouver+Canada",
            "head+of+strategy+Vancouver+Canada",
            "director+transformation+Vancouver+Canada",
            "senior+manager+strategy+Canada+remote+$120k",
        ],
        "linkedin_keywords": [
            "director operations Vancouver",
            "director strategy Vancouver",
            "senior manager operations Vancouver $120k",
            "chief of staff Vancouver",
            "head of business operations Canada",
        ],
        "companies": [
            ("Telus", "https://careers.telus.com/"),
            ("lululemon", "https://careers.lululemon.com/"),
            ("RBC", "https://jobs.rbc.com/"),
            ("TD Bank", "https://jobs.td.com/"),
            ("CIBC", "https://www.cibc.com/careers/"),
            ("BMO", "https://bmo.com/careers/"),
            ("Scotiabank", "https://careers.scotiabank.com/"),
            ("YVR", "https://careers.yvr.ca/"),
            ("Aritzia", "https://aritzia.com/careers/"),
            ("Vancity", "https://vancity.com/careers/"),
            ("BC Hydro", "https://app.bchydro.com/careers/"),
            ("Rogers", "https://careers.rogers.com/"),
            ("Bell", "https://bell.ca/careers/"),
            ("ICBC", "https://icbc.com/careers/"),
            ("Canada Goose", "https://careers.canadagoose.com/"),
            ("Loblaw", "https://careers.loblaw.ca/"),
            ("TransLink", "https://careers.translink.ca/"),
            ("Enbridge", "https://careers.enbridge.com/"),
            ("Suncor", "https://careers.suncor.com/"),
            ("CN Rail", "https://www.cn.ca/en/careers/"),
        ],
    },
    "Consulting": {
        "label": "📊 CONSULTING",
        "description": "Global MBB+Big4, Canadian firms, boutique, advisory",
        "hiring_cafe_queries": [
            "senior+manager+strategy+consulting+Vancouver+Canada",
            "director+operations+consulting+Canada",
            "management+consultant+senior+Vancouver+Canada",
            "engagement+manager+strategy+Vancouver",
            "senior+consultant+operations+Vancouver+Canada",
            "director+transformation+consulting+Canada",
        ],
        "linkedin_keywords": [
            "strategy consulting manager Vancouver",
            "management consultant senior Vancouver",
            "operations consulting director Canada",
            "senior manager consulting Vancouver advisory",
            "engagement manager strategy Canada",
        ],
        "companies": [
            ("McKinsey", "https://www.mckinsey.com/careers/"),
            ("BCG", "https://careers.bcg.com/"),
            ("Bain", "https://www.bain.com/careers/"),
            ("EY", "https://careers.ey.com/"),
            ("Deloitte", "https://careers.deloitte.ca/"),
            ("KPMG", "https://careers.kpmg.ca/"),
            ("PwC", "https://careers.pwc.com/"),
            ("Accenture", "https://www.accenture.com/ca-en/careers/"),
            ("BDO", "https://www.bdo.ca/careers/"),
            ("MNP", "https://www.mnp.ca/en/careers"),
            ("Slalom", "https://www.slalom.com/careers"),
            ("IBM Consulting", "https://www.ibm.com/ca-en/consulting/"),
            ("Huron", "https://www.huron.com/careers/"),
            ("Oliver Wyman", "https://www.oliverwyman.com/careers/"),
            ("LEK", "https://www.lek.com/careers/"),
            ("AlixPartners", "https://www.alixpartners.com/careers/"),
            ("Kearney", "https://www.kearney.com/careers/"),
            ("Gartner", "https://www.gartner.com/careers/"),
        ],
    },
    "SaaS": {
        "label": "☁️ SAAS / TECH",
        "description": "B2B SaaS, platform companies, tech-enabled (Canadian + US-in-Canada)",
        "hiring_cafe_queries": [
            "director+revenue+operations+SaaS+Vancouver+Canada",
            "director+operations+SaaS+Vancouver+Canada",
            "head+of+revenue+operations+Canada+remote",
            "chief+of+staff+tech+Vancouver+Canada",
            "director+business+operations+SaaS+Canada",
            "vp+operations+SaaS+Vancouver+Canada",
            "revenue+operations+manager+Canada+remote+$120k",
            "operations+director+software+Vancouver+Canada",
        ],
        "linkedin_keywords": [
            "revenue operations director Canada",
            "director operations SaaS Vancouver",
            "chief of staff tech Vancouver",
            "head of revenue operations Vancouver",
            "director business operations SaaS Canada",
            "senior manager operations technology Vancouver",
        ],
        "companies": [
            ("Clio", "https://www.clio.com/about/careers/"),
            ("Procurify", "https://procurify.com/careers/"),
            ("Jobber", "https://jobber.com/careers/"),
            ("1Password", "https://1password.com/jobs/"),
            ("Wrapbook", "https://wrapbook.com/careers/"),
            ("Shopify", "https://www.shopify.com/careers/"),
            ("Copper", "https://www.copper.com/careers/"),
            ("Thinkific", "https://www.thinkific.com/careers/"),
            ("FreshBooks", "https://www.freshbooks.com/careers/"),
            ("Wealthsimple", "https://www.wealthsimple.com/en-ca/careers"),
            ("Lightspeed", "https://www.lightspeedhq.com/careers/"),
            ("Hootsuite", "https://careers.hootsuite.com/"),
            ("Visier", "https://www.visier.com/careers/"),
            ("MediaValet", "https://mediavalet.com/careers/"),
            ("Hiive", "https://www.hiive.com/careers"),
            ("Benji Pays", "https://benjipays.com/careers/"),
            ("Minga", "https://minga.io/careers/"),
            ("Practice Better", "https://practicebetter.com/careers/"),
            ("Leap Tools", "https://www.leaptools.com/careers/"),
            ("EviSmart", "https://evismart.com/careers/"),
            ("Xero", "https://www.xero.com/careers/"),
            ("Zendesk", "https://www.zendesk.com/jobs/"),
            ("HubSpot", "https://www.hubspot.com/careers/"),
            ("Intercom", "https://www.intercom.com/careers/"),
            ("Stripe", "https://stripe.com/jobs/"),
            ("Twilio", "https://www.twilio.com/company/jobs/"),
            ("Asana", "https://asana.com/jobs/"),
            ("Monday", "https://monday.com/careers/"),
            ("Notion", "https://www.notion.so/careers/"),
            ("Canva", "https://www.canva.com/careers/"),
            ("Atlassian", "https://www.atlassian.com/company/careers/"),
            ("Datadog", "https://www.datadoghq.com/careers/"),
            ("Snowflake", "https://careers.snowflake.com/"),
            ("Workday", "https://www.workday.com/careers/"),
            ("ServiceNow", "https://careers.servicenow.com/"),
        ],
    },
    "BigTech": {
        "label": "🔵 BIG TECH / US-IN-CANADA",
        "description": "FAANG + tier-2 US tech with Vancouver/Canada offices",
        "hiring_cafe_queries": [
            "program+manager+Amazon+Vancouver+Canada",
            "operations+Google+Vancouver+Canada",
            "strategy+operations+Microsoft+Vancouver+Canada",
            "program+manager+Apple+Vancouver+Canada",
            "business+operations+Meta+Vancouver+Canada",
            "operations+Salesforce+Vancouver+Canada",
            "program+manager+Uber+Vancouver+Canada",
            "program+manager+NVIDIA+Vancouver+Canada",
        ],
        "linkedin_keywords": [
            "program manager Amazon Vancouver",
            "operations Google Vancouver",
            "strategy operations Microsoft Vancouver",
            "program manager tech Vancouver $120k",
            "business operations Uber Vancouver",
            "operations DoorDash Canada",
        ],
        "companies": [
            ("Amazon", "https://www.amazon.jobs/"),
            ("Google", "https://careers.google.com/"),
            ("Meta", "https://www.metacareers.com/"),
            ("Apple", "https://www.apple.com/careers/"),
            ("Microsoft", "https://careers.microsoft.com/"),
            ("Netflix", "https://jobs.netflix.com/"),
            ("NVIDIA", "https://www.nvidia.com/careers/"),
            ("Salesforce", "https://www.salesforce.com/company/careers/"),
            ("Uber", "https://www.uber.com/careers/"),
            ("DoorDash", "https://careers.doordash.com/"),
            ("Airbnb", "https://careers.airbnb.com/"),
            ("Block/Square", "https://block.xyz/careers/"),
            ("PayPal", "https://www.paypal.com/careers/"),
            ("Zoom", "https://careers.zoom.us/"),
            ("Palo Alto Networks", "https://www.paloaltonetworks.com/careers/"),
            ("Qualcomm", "https://www.qualcomm.com/careers/"),
            ("AMD", "https://www.amd.com/careers/"),
        ],
    },
    "Startups": {
        "label": "🚀 STARTUPS",
        "description": "US + Canadian, seed to Series C, growth-stage, remote-first",
        "hiring_cafe_queries": [
            "head+of+operations+startup+Vancouver+Canada",
            "chief+of+staff+startup+Vancouver+Canada",
            "director+operations+startup+Vancouver+Canada",
            "revenue+operations+startup+Canada+remote",
            "operations+lead+startup+Vancouver+Canada",
            "director+operations+startup+Canada+remote+$120k",
            "COO+startup+Vancouver+Canada",
        ],
        "linkedin_keywords": [
            "head of operations startup Vancouver",
            "chief of staff startup Vancouver",
            "director operations startup Canada",
            "revenue operations startup Canada remote",
            "operations lead early stage Vancouver",
        ],
        "companies": [
            ("Brex", "https://www.brex.com/careers/"),
            ("Rippling", "https://www.rippling.com/careers/"),
            ("Deel", "https://www.deel.com/careers/"),
            ("Vanta", "https://www.vanta.com/careers/"),
            ("Ramp", "https://ramp.com/careers/"),
            ("Aiven", "https://aiven.io/careers/"),
            ("EviSmart", "https://evismart.com/careers/"),
            ("Benji Pays", "https://benjipays.com/careers/"),
            ("Hiive", "https://www.hiive.com/careers"),
            ("Minga", "https://minga.io/careers/"),
            ("Practice Better", "https://practicebetter.com/careers/"),
            ("Wrapbook", "https://wrapbook.com/careers/"),
            ("Procurify", "https://procurify.com/careers/"),
            ("Jobber", "https://jobber.com/careers/"),
            ("Copper", "https://www.copper.com/careers/"),
        ],
    },
}

PIPE_KEYS = list(PIPES.keys())

PIPE_MAP = {
    "brex": "Startups",
    "evismart": "SaaS",
    "thinkific": "SaaS",
    "practicebetter": "SaaS",
    "hootsuite": "SaaS",
}

OPS_TITLES = [
    "director of operations", "director of strategy", "director of revenue operations",
    "head of operations", "head of strategy", "head of revenue operations",
    "vp operations", "vp of operations", "chief of staff", "general manager",
    "senior manager operations", "senior manager strategy",
    "manager operations", "manager strategy",
    "director of business operations", "director strategic planning",
    "director of program management", "operations director",
    "strategy director", "revops", "revenue operations",
    "coo", "chief operating officer", "gm",
    "head of business operations", "director transformation",
    "senior manager", "manager", "director", "lead",
    "program manager", "product operations",
]

def is_ops_relevant(title):
    t = title.lower()
    return any(phrase in t for phrase in OPS_TITLES)

def teer_estimate(title):
    t = title.lower()
    if any(x in t for x in ["director","vp","head of","chief of","coo"]):
        return 0
    if any(x in t for x in ["manager","lead","senior"]):
        return 0
    return 1

# ──────────────────────────────────────────────
# MASTER CORPUS LOADER (for scoring)
# ──────────────────────────────────────────────

def load_corpus():
    if not CORPUS_FILE.exists():
        return {"modules": [], "keywords": []}
    text = CORPUS_FILE.read_text()
    keywords = []
    core = [
        "organizational scaling", "revenue operations", "strategic planning",
        "okr", "cross-functional", "leadership", "compliance", "financial modeling",
        "p&l", "m&a", "due diligence", "integration", "hiring", "process design",
        "board reporting", "change management", "kpi", "forecasting",
        "crm", "salesforce", "sop", "go-to-market", "gtm",
        "systems", "playbook", "scalability", "transformation",
        "executive partnership", "chief of staff", "program management",
        "vendor management", "budget", "stakeholder",
        "arr", "cac", "ltv", "pipeline coverage", "sales velocity",
        "multi-site", "multi-location", "resource allocation",
        "workflow", "dashboard", "data integrity", "governance",
        "earnout", "due diligence", "workstream",
    ]
    keywords.extend(core)
    return {"keywords": list(set(k.lower() for k in keywords))}

def score_job(title, description=""):
    corpus = load_corpus()
    kw = corpus["keywords"]
    text = (title + " " + description).lower()
    matches = sum(1 for k in kw if k.lower() in text)
    total = len(kw)
    if total == 0:
        return 0, {"matched": 0, "total": 0, "matched_terms": []}
    matched_terms = [k for k in kw if k.lower() in text][:20]
    raw_score = (matches / min(total, 100)) * 100
    title_bonus = 10 if any(t in title.lower() for t in ["director", "vp", "head of", "chief of", "manager", "lead"]) else 0
    ops_bonus = 5 if any(t in title.lower() for t in ["operations", "strategy", "revenue", "program", "business"]) else 0
    fit = min(round(raw_score + title_bonus + ops_bonus), 99)
    return fit, {"matched": matches, "total": total, "title_bonus": title_bonus, "ops_bonus": ops_bonus, "matched_terms": matched_terms}

# ──────────────────────────────────────────────
# GREENHOUSE AUTO-FETCH
# ──────────────────────────────────────────────

def fetch_greenhouse_all():
    print(f"\n  {'='*50}")
    print(f"  TIER 1 — GREENHOUSE AUTO-FETCH ({len(GREENHOUSE_BOARDS)} working boards)")
    print(f"  {'='*50}")
    results = []
    for company, board in GREENHOUSE_BOARDS.items():
        try:
            url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code != 200:
                continue
            data = r.json()
            jobs = data.get("jobs", [])
            for job in jobs:
                title = job.get("title", "")
                loc = job.get("location", {}).get("name", "")
                loc_lower = loc.lower()
                if not loc_lower:
                    continue
                # Keep Canada jobs only
                if not any(x in loc_lower for x in ["canada", "vancouver", "british columbia", "remote", "toronto"]):
                    continue
                url_job = job.get("absolute_url", "")
                fit, details = score_job(title)
                results.append({
                    "source": f"Greenhouse ({company})",
                    "company": company,
                    "title": title,
                    "location": loc,
                    "url": url_job,
                    "fit": fit,
                    "details": details,
                    "salary": "",
                    "posted": "",
                })
            print(f"     {company:20s} → {len(jobs):3d} total, {len([j for j in jobs if 'canada' in j.get('location',{}).get('name','').lower() or 'vancouver' in j.get('location',{}).get('name','').lower()]):3d} Canada-relevant")
        except Exception as e:
            print(f"     {company:20s} → ✗ {str(e)[:40]}")
    return results

# ──────────────────────────────────────────────
# SCORING & DISPLAY
# ──────────────────────────────────────────────

def print_full_table(all_jobs, label="ALL"):
    """Print ALL jobs in the full table format — every source, every job."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(all_jobs)
    ops_count = sum(1 for j in all_jobs if j.get("ops", False))
    all_jobs.sort(key=lambda j: (-j.get("ops", False), -j["fit"]))

    print(f"\n{'='*90}")
    print(f"  JOBS OS 2026 — FETCH v2    │  {now}  │  {label} ({total} jobs, {ops_count} ops)")
    print(f"{'='*90}")
    print()
    print(f"{'█'*90}")
    print(f"  ALL JOBS — # │ Company │ Role │ TEER │ Fit% │ Ops? │ Pipe │ Source")
    print(f"{'█'*90}")
    print()
    print(f"{'─'*90}")
    print(f"  # │ Company         │ Role                                              │ TEER│ Fit%│ Ops?│ Pipe           │ Source")
    print(f"{'─'*90}")

    for i, j in enumerate(all_jobs, 1):
        title = j["title"][:53]
        company = j["company"][:15]
        pipe_label = j.get("pipe_label", "☁️ SaaS/Tech")[:14]
        fit = j["fit"]
        teer = j.get("teer", teer_estimate(j["title"]))
        ops = "✓" if j.get("ops", False) else " "
        print(f" {i:2d} │ {company:15s} │ {title:53s} │ {teer}    │ {fit:2d}%  │  {ops}  │ {pipe_label:14s} │ {j['source']}")

    print(f"{'─'*90}")
    print(f"\n  🔥 {ops_count} ops-relevant of {total} total\n")

def print_pipe_results(pipe_name, gh_results):
    """Legacy — keeps per-pipe summary for compatibility."""
    pass

def print_pipe_urls(pipe_name):
    pipe = PIPES[pipe_name]
    label = pipe["label"]

    print(f"\n  {'─'*60}")
    print(f"  {label}")
    print(f"  {'─'*60}")

    # HiringCafe URLs (for opening in browser)
    print(f"\n  🔍 HIRINGCAFE SEARCHES (open in browser):")
    for q in pipe["hiring_cafe_queries"]:
        url = f"https://hiring.cafe/search?q={q}"
        print(f"     {url}")

    # LinkedIn URLs
    print(f"\n  🔗 LINKEDIN CROSS-CHECK (open in browser):")
    for kw in pipe["linkedin_keywords"]:
        encoded = kw.replace(" ", "%20").replace("$", "%24")
        url = f"https://ca.linkedin.com/jobs/search/?keywords={encoded}&f_TPR=r86400"
        print(f"     {url}")

    # Career pages
    print(f"\n  🏢 COMPANY CAREER PAGES:")
    for name, url in pipe["companies"]:
        print(f"     {name:25s} → {url}")

# ──────────────────────────────────────────────
# OUTPUT FILE WRITER
# ──────────────────────────────────────────────

def write_pipeline_file(all_gh_results, all_annotated=None):
    ts = datetime.now().strftime("%b %d, %Y %H:%M")
    total = len(all_annotated) if all_annotated else sum(len(v) for v in all_gh_results.values())
    ops_count = sum(1 for j in (all_annotated or [])) if all_annotated else 0

    output = f"""# WIDE NET FETCH RESULTS — Cast Wide, Filter Hard
## {ts} | Hybrid Source Stack: Greenhouse Auto-Fetch + HiringCafe + LinkedIn Cross-Check
## 24h Recency enforced via browser | $120K+ | TEER 0/1 | Ops Roles
## US-headquartered companies with Canada roles = FULLY valid (same PR treatment)

---

## FULL TABLE — ALL {total} CANADA-RELEVANT JOBS

| # | Company | Role | TEER | Fit% | Ops? | Pipe | Source |
|---|---------|------|------|------|------|------|--------|
"""
    if all_annotated:
        for i, j in enumerate(all_annotated, 1):
            pipe_label = PIPES.get(j.get("pipe", "SaaS"), {}).get("label", "☁️ SaaS/Tech")[:14]
            ops = "✓" if j.get("ops", False) else " "
            output += f"| {i} | {j['company']} | {j['title'][:53]} | {j.get('teer', 1)} | {j['fit']}% | {ops} | {pipe_label} | {j['source']} |\n"

    output += f"""
**Ops-relevant: {ops_count} of {total} | ⚠️ GH API has no 24h filter — these are ALL open jobs**

---

### SOURCE ARCHITECTURE
| Tier | Source | Method |
|------|--------|--------|
| 1 | **Greenhouse API** | Auto-fetched ({len(GREENHOUSE_BOARDS)} working boards) |
| 2 | **HiringCafe** | Manual browser — search URLs generated below |
| 3 | **LinkedIn Jobs** | Cross-check — verify shortlisted roles |
| 4 | **Company career pages** | Direct links — manual browsing |

### PIPELINE SUMMARY
| Pipe | Auto-Fetched (GH) | Tier 1 (≥80%) | Tier 2 (60-79%) |
|------|-------------------|---------------|-----------------|
"""
    for pipe_name in PIPE_KEYS:
        results = all_gh_results.get(pipe_name, [])
        t1 = len([r for r in results if r["fit"] >= 80])
        t2 = len([r for r in results if 60 <= r["fit"] < 80])
        pipe = PIPES[pipe_name]
        output += f"| {pipe['label']} | {len(results)} | {t1} | {t2} |\n"

    for pipe_name in PIPE_KEYS:
        pipe = PIPES[pipe_name]
        results = all_gh_results.get(pipe_name, [])

        output += f"""

### {pipe['label']}
*{pipe['description']}*

**Auto-Fetched from Greenhouse:**

| # | Company | Role | Fit | Location | Source |
|---|---------|------|-----|----------|--------|
"""
        sorted_results = sorted(results, key=lambda r: -r["fit"])
        if sorted_results:
            for i, j in enumerate(sorted_results, 1):
                output += f"| {i} | **{j['company']}** | {j['title'][:50]} | **{j['fit']}%** | {j['location'][:30]} | {j['source']} |\n"
        else:
            output += "| — | — | No auto-fetched roles | — | — | — |\n"

        output += f"""
**HiringCafe Search URLs (open in browser):**
"""
        for q in pipe["hiring_cafe_queries"]:
            output += f"- https://hiring.cafe/search?q={q}\n"

        output += f"""
**LinkedIn Cross-Check URLs (open in browser):**
"""
        for kw in pipe["linkedin_keywords"]:
            encoded = kw.replace(" ", "%20").replace("$", "%24")
            output += f"- https://ca.linkedin.com/jobs/search/?keywords={encoded}&f_TPR=r86400\n"

    output += f"""

---

### WORKING GREENHOUSE BOARDS
| Company | Jobs | Canada |
|---------|------|--------|
"""
    for company, board in GREENHOUSE_BOARDS.items():
        try:
            r = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs", headers=HEADERS, timeout=8)
            if r.status_code == 200:
                data = r.json()
                jobs = data.get("jobs", [])
                canada = sum(1 for j in jobs if 'canada' in j.get('location',{}).get('name','').lower() or 'vancouver' in j.get('location',{}).get('name','').lower())
                output += f"| {company} | {len(jobs)} | {canada} |\n"
        except:
            output += f"| {company} | — | — |\n"

    output += f"""

---

### NEXT STEPS
1. **Open each HiringCafe URL** in browser → search with 24h filter → identify ops-relevant roles
2. **Cross-check shortlisted roles** on LinkedIn (open cross-check URLs)
3. **Score each role** (paste JD into `--score` mode or route through me)
4. **Run `SHOOT [company]`** to deploy full 13-section package for each priority role
5. **Record submissions** in data/jobs.json
6. **Run FETCH again** in 24h — fresh recency window

*Generated by FETCH ENGINE v2 — Hybrid Architecture*
"""

    OUTPUT_FILE.write_text(output)
    print(f"\n  ✓ Pipeline written to: {OUTPUT_FILE.name}")

# ──────────────────────────────────────────────
# SCORE PASTE MODE
# ──────────────────────────────────────────────

def score_paste():
    print("\n  Paste job title + description (Ctrl+D to finish):")
    try:
        text = sys.stdin.read().strip()
    except:
        text = ""
    if not text:
        print("  No input.")
        return
    lines = text.split("\n")
    title = lines[0].strip()
    desc = " ".join(lines[1:])
    fit, details = score_job(title, desc)
    terms = details["matched_terms"]
    print(f"\n{'='*60}")
    print(f"  SCORE: {fit}%")
    print(f"{'='*60}")
    print(f"  Title: {title}")
    print(f"  Keywords matched: {details['matched']}/{min(details['total'], 100)}")
    if terms:
        print(f"  Top matches: {', '.join(terms[:10])}")
    print()
    if fit >= 80:
        print("  VERDICT: 🔥 PRIORITY — Apply immediately")
    elif fit >= 60:
        print("  VERDICT: 👍 SECONDARY — Apply with positioning")
    else:
        print("  VERDICT: 👎 PASS — Not worth precision investment")

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    print(f"{'='*60}")
    print(f"  JOBS OS 2026 — FETCH ENGINE v2 (Hybrid Architecture)")
    print(f"  Auto-fetch (Greenhouse) + HiringCafe + LinkedIn cross-check")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    if "--score" in sys.argv:
        score_paste()
        return

    if "--urls" in sys.argv:
        for pipe_name in PIPE_KEYS:
            print_pipe_urls(pipe_name)
        return

    single_pipe = None
    for arg in sys.argv:
        if arg.startswith("--pipe="):
            single_pipe = arg.split("=", 1)[1]
        elif arg == "--pipe" and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            single_pipe = sys.argv[idx + 1]

    if single_pipe and single_pipe not in PIPES:
        print(f"  [!] Unknown pipe: {single_pipe}")
        print(f"  Available: {', '.join(PIPE_KEYS)}")
        return

    targets = [single_pipe] if single_pipe else PIPE_KEYS

    # Step 1: Auto-fetch from Greenhouse
    print(f"\n{'='*60}")
    print(f"  PHASE 1 — AUTO-FETCH (Greenhouse API)")
    print(f"{'='*60}")
    all_gh = fetch_greenhouse_all()

    # Step 2: Route GH results to pipes
    gh_by_pipe = {p: [] for p in PIPE_KEYS}

    # Map companies to pipes
    company_to_pipe = {}
    for pn, pipe in PIPES.items():
        for name, _ in pipe["companies"]:
            company_to_pipe[name.lower()] = pn

    for r in all_gh:
        cn = r["company"].lower()
        if cn in company_to_pipe:
            gh_by_pipe[company_to_pipe[cn]].append(r)
        else:
            # Unmapped GH companies — assign to Startups or SaaS by guess
            gh_by_pipe["Startups"].append(r)

    print(f"\n  Total auto-fetched: {len(all_gh)} Canada-relevant jobs")

    # Step 3: Build full annotated list with ops/pipe info
    all_annotated = []
    board_to_pipe = {
        "brex": "Startups", "hootsuite": "SaaS", "evismart": "SaaS",
        "thinkific": "SaaS", "practicebetter": "SaaS",
    }
    for r in all_gh:
        board_key = GREENHOUSE_BOARDS.get(r["company"], "")
        pipe_name = board_to_pipe.get(board_key, "Startups")
        all_annotated.append({
            **r,
            "board": board_key,
            "pipe": pipe_name,
            "ops": is_ops_relevant(r["title"]),
            "teer": teer_estimate(r["title"]),
        })
    all_annotated.sort(key=lambda j: (-j["ops"], -j["fit"]))

    # Step 4: Show ALL jobs in full table — Greenhouse auto-fetch
    print_full_table(all_annotated, "AUTO-FETCH (Greenhouse)")

    # Step 5: Print per-pipe HiringCafe URLs for browser
    print(f"{'█'*90}")
    print(f"  TIER 3 — HIRINGCAFE URLs (open in browser, set 24h filter)")
    print(f"{'█'*90}")
    for pipe_name in targets:
        print_pipe_urls(pipe_name)

    print(f"\n{'='*60}")
    print(f"  NEXT ACTION:")
    print(f"{'='*60}")
    print(f"  1. Open HiringCafe URLs in browser — 24h filter")
    print(f"  2. Find ops roles ≥60% fit, $120K+, TEER 0/1")
    print(f"  3. Paste JD → I SHOOT 13-section package")

    if not single_pipe:
        write_pipeline_file(gh_by_pipe, all_annotated)

    print(f"\n  ✓ FETCH v2 complete — {datetime.now().strftime('%H:%M:%S')}")
    print()

if __name__ == "__main__":
    main()
