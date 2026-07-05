---
name: auto-scan
version: "1.0.0"
description: >
  Auto-scan job portals via 49 ATS provider modules.
  Runs career-ops scanner to discover jobs from Greenhouse, Lever, Ashby, Workday, etc.
  Use when user wants to auto-discover jobs, scan company career pages, or verify job liveness.
triggers:
  - command: SCAN
    description: "Run 49 ATS providers to auto-discover jobs"
    options:
      - "--company [name]" : Scan single company
      - "--verify" : Playwright-check URLs, drop expired
      - "--fresh" : Only 24h fresh results
      - "--providers" : List available providers
  - command: INTEL
    description: "Run social intelligence on target company"
  - command: DOCTOR
    description: "Check what intelligence/scanner tools are working"
---

# AUTO-SCAN SKILL — career-ops Scanner Adapter

## Location
Scanner engine: `lib/career-ops/scan.mjs`
Config: `lib/career-ops/portals.yml`
Profile: `lib/career-ops/config/profile.yml`

## Commands

### SCAN — Auto-Discover Jobs

```bash
# Full scan — all enabled tracked companies
node lib/career-ops/scan.mjs

# Single company
node lib/career-ops/scan.mjs --company "Human Agency"

# Verify URLs with Playwright (drop expired)
node lib/career-ops/scan.mjs --verify

# Dry run — preview without writing files
node lib/career-ops/scan.mjs --dry-run
```

**Output:** Each job has `{ title, url, company, location, postedAt }`.

### SCAN --fresh — Only 24h Fresh

Pipe scan output through a 24h window filter. Results merge into the FETCH pipeline.

### SCAN --verify — Liveness Check

Batch-verify all URLs in your CURATED pipeline. Drops expired postings. Uses Playwright for anti-bot career pages.

### DOCTOR — Health Check

```bash
node lib/career-ops/doctor.mjs
```

## Integration with FETCH

When user runs FETCH:
1. Also run `node lib/career-ops/scan.mjs --company [target]` for each high-priority company
2. Merge results with manual board search results
3. Dedup by URL
4. Present in unified CURATED_30 format

## Notes
- Zero-token scanning — pure HTTP/JSON, no AI calls
- Non-ATS boards fall back to WebSearch
- New companies can be added to portals.yml at any time
