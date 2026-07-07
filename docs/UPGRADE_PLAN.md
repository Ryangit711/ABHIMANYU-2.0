# UPGRADE PLAN — ABHIMANYU 2.0 Source Expansion + Career-Ops Integration

**Date:** 2026-07-07
**Status:** Active

---

## Phase 1: SYSTEM SOURCES Expansion

### A. Job Boards (13 → 18+)

| Board | URL | Why Added |
|-------|-----|-----------|
| **Wellfound (AngelList)** | wellfound.com | S pipe startup jobs |
| **WorkBC** | workbc.ca | Official BC job bank, TEER 0/1 filterable |
| **Crabjobs** | crabjobs.ca | Canadian tech/startup listings |
| **Vancouver Tech Jobs** | vanhiring.com | Vancouver-specific curated |
| **RemoteOK** | remoteok.com | Remote Canada ops roles |
| **WeWorkRemotely** | weworkremotely.com | Remote Canada ops roles |

### B. Company Career Pages → Sector Tiers

**T Pipe (Tech/BigTech):**
- Tier 1 FAANG: Amazon, Microsoft, Google Vancouver
- Tier 2 US-in-Canada: DoorDash, Indeed, Uber, Brex, Stripe, HubSpot, Block/Square
- Tier 3 Canadian Tech: Shopify, Clio, 1Password, Wealthsimple, Jobber, D2L, Hootsuite, Copper
- Tier 4 Scale-ups: Procurify, Ada, Hiive, Thinkific, Trulioo, Marqeta, Zenoti

**C Pipe (Consulting):**
- Tier 1 MBB: McKinsey, BCG, Bain
- Tier 2 Big4: Deloitte Canada, EY Canada, KPMG Canada, PwC Canada
- Tier 3 Boutique: Slalom, OC&C, A&M, LEK, West Monroe, Kearney
- Tier 4 Tech-adjacent: Accenture, Infosys Canada, TCS Canada, CGI

**I Pipe (Internal Strategy/Corporate):**
- Tier 1 Telco: TELUS, Rogers, Bell
- Tier 2 Retail: lululemon, Aritzia, Arc'teryx, MEC, LUSH
- Tier 3 Healthcare: Providence Health, BC Cancer, Fraser Health, Vancouver Coastal Health
- Tier 4 Energy/Infra: BC Hydro, Methanex, FortisBC, Trans Mountain
- Tier 5 Government: City of Vancouver, Province of BC, TransLink

**S Pipe (Startups):**
- Tier 1 Funded $50M+: Brex, EvenUp, Hiive
- Tier 2 Growth $10-50M: Ada, Procurify, Copper, Remarcable, Trulioo
- Tier 3 Early <$10M: Practice Better, EviSmart, Human Agency, Zenoti, SOCi

---

## Phase 2: ATS Coverage Expansion (6 → 20+)

New ATS platforms added to ATS_ESOTERICA.md:

| Provider | Used By | Source |
|----------|---------|--------|
| Ashby | 1Password, Procurify, Trulioo | career-ops |
| SmartRecruiters | AECOM, mid-market | career-ops |
| BambooHR | Small/mid Canadian companies | career-ops |
| Breezy | Startups | career-ops |
| Personio | EU companies with Canada offices | career-ops |
| Recruitee | Canadian tech | career-ops |
| TeamTailor | Nordic companies in Canada | career-ops |
| Workable | Aviso Wealth, mid-market | career-ops |
| Rippling | Modern startups | career-ops |
| Avature | IBM, large enterprises | career-ops |
| Pinpoint | Growing Canadian startups | career-ops |
| JibeApply | Legacy Oracle-ish | career-ops |
| Comeet | Mid-market | career-ops |
| Oracle Cloud | Various | existing |

---

## Phase 3: Career-Ops Feature Porting

| Feature | Description | Integration Point |
|---------|-------------|-------------------|
| Multi-level scan | local → Playwright → HTTP JSON API → WebSearch | FETCH engine |
| Title/content/location/salary filters | Port portal.yml config | QBIT 2 collapse |
| Ghost job detection | liveness-core.mjs + check-liveness.mjs | Post-FETCH validation |
| EVAL scoring (A-F, 10 dims) | process-quality.mjs | OPS_EVAL_CRITERIA.md → EVAL_V2 |
| Contact discovery (contacto) | modes/contacto.md | SHOOT Section 14 |
| Dashboard TUI | build-dashboard.mjs | New command (optional) |
| Interview story bank | STAR+Reflection accum | interview-prep skill |
| Pipeline integrity | merge, dedup, status checks | PIPELINE.md system |

---

## Phase 4: Implementation Sequence

```
WEEK 1:
  Day 1: Write UPGRADE_PLAN.md → expand SYSTEM_SOURCES.md with boards + company tiers
  Day 2-3: Port career-ops ATS providers (create lib/ats-providers/) 
            → update ATS_ESOTERICA.md with new platforms
  Day 4-5: Integrate title/content/location/salary filters into FETCH collapse logic
  
WEEK 2:
  Day 1-2: Port ghost job detection → add to FETCH output as ⚠️ flag
  Day 3-4: Port EVAL scoring (enhance OPS_EVAL_CRITERIA.md → EVAL_V2_CRITERIA.md)
  Day 5: Port contact discovery → integrate into SHOOT Section 14

WEEK 3:
  Day 1-2: Install browser-use + Playwright → make AUTO-APPLY work on T480
  Day 3-4: Install Scrapling → stealth FETCH scanner (Cloudflare bypass)
  Day 5: Test full pipeline end-to-end → commit
```

---

## Additive-Only Guarantee

Every existing command, file, protocol stays intact. Nothing removed. Career-ops providers augment our ATS layer. Company tiers organize not replace. The thinker still decides.

**All changes are additive. Zero deletions. Zero regressions.**
