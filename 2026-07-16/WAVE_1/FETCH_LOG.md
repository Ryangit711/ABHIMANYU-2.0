# FETCH LOG — 2026-07-16

## Scan Results

| Metric | Value |
|--------|-------|
| Scanner | career-ops `scan.mjs` |
| Companies scanned | 18 |
| Job boards scanned | 39 |
| Total jobs found | 7,897 |
| Filtered by title | 5,825 removed |
| Filtered by location | 1,957 removed |
| Duplicates skipped | 86 |
| **New offers added** | **29** |
| Aman-relevant (post-filter) | ~4 |

## New Scanned Offers — Relevance Check

| # | Company | Role | Location | Relevant? | Reason |
|:-:|---------|------|----------|:---------:|--------|
| 1 | Marqeta | Assistant Manager, Bank Partnerships | Vancouver/Toronto | ⚠️ | Fintech, not bank. "Assistant Mgr" may be junior. No credit check requirement found. |
| 2 | Marqeta | Due Diligence Senior Analyst | Vancouver/Toronto | ⚠️ | Due diligence role, credit check risk. "Sr Analyst" may be below salary floor. |
| 3 | Eluta.ca | Operations Manager | Canada | ✅ | Unknown employer (scraped listing). Need to investigate actual company. |
| 4 | Eluta.ca | (CAN) Mgr, Technology Operations | Canada | ⚠️ | Tech ops — may require technical depth outside Aman's scope. |
| 5-29 | Various | US/Germany/Poland/Brazil/Spain/EU | International | ❌ | Outside Vancouver/Remote Canada requirement |

## Scanner Status

The career-ops `scan.mjs` is now **fully operational** on this machine (tested with 18 supported ATS providers + 39 job boards).

### Working Sources (ATS-supported)
- **Greenhouse:** Brex, OpenTable, Human Agency, Marqeta, Zenoti, SOCi, Thinkific
- **Ashby:** 1Password, Procurify, Trulioo
- **Lever:** Wealthsimple
- **Workday:** Clio
- **SuccessFactors:** TELUS, Deloitte Canada, EY Canada
- **SmartRecruiters:** AECOM
- **Workable:** Aviso Wealth
- **Amazon Jobs** (direct API)

### Failing Sources (need investigation)
- Monster Canada RSS — HTTP 503
- SolidJobs — API path format mismatch
- JustJoin.it — URL trust validation
- CollabWork, Remote Rocketship, GoFractional, FractionalJobs, Cerius Executives — network errors

### Empty Sources (live but no matching jobs)
- Wealthsimple, Aviso Wealth, AECOM

## Pipeline Impact

- 29 new offers added to `career-ops/data/pipeline.md`
- No new Aman-strong targets discovered this cycle
- Existing CURATED_30 targets remain the primary focus
- Scanner will find more over time as new postings appear

## Recommendation

Continue with existing pipeline. Rescan in 24h for fresh postings. For now, the highest-leverage action remains: **submit Brex via Greenhouse**.
