---
name: networking-cadence
description: "Auto-triggered after YES (approval) — no SUBMITTED command needed. Reads pipeline for submission date, auto-starts T+0→T+28 timer. Proactive prompts at T+0, T+3, T+7, T+14. Cross-wired: receives signal from shoot-deployer + pipeline-tracker, writes to networking_log.json, displays in AUTO-NETWORKING footer."
---

# NETWORKING CADENCE — Auto-Triggered Outreach Timer

## Cross-Skill Wiring

### Inputs (Read From)
| Source | What | When |
|--------|------|------|
| `shoot-deployer` (auto-signal after YES) | company, T+0=today, personas from SHOOT section 13 | On YES |
| `pipeline-tracker` (auto-signal on ✅) | company, role, submission date | On pipeline update |
| `data/pipeline/PIPELINE.md` | All submitted jobs with T+ dates | Every response (footer check) |
| SHOOT package | Personas + message templates for each company | On YES |

### Outputs (Write To)
| Target | What | When |
|--------|------|------|
| `data/networking_log.json` | Cadence entries (company, T+ dates, personas, sent status) | On YES + on each action completed |
| `data/pipeline/PIPELINE.md` | Update next_action for follow-up items | On cadence advance |

---

## Execution: On YES (Auto-Trigger from shoot-deployer)

```
1. RECEIVE signal from shoot-deployer:
   → company, role, T+0 = today
   → personas from SHOOT section 13 (IC/Associate, Manager/Director, Sr IC/Manager, Exec Sponsor)
   → message templates for each persona

2. WRITE to data/networking_log.json:
   {
     "company": "[name]",
     "role": "[title]",
     "submitted_date": "YYYY-MM-DD",
     "cadence": {
       "T+0": {"action": "Submit application", "done": false},
       "T+3": {"action": "Connect with IC/Associate", "persona": "IC/Associate", "done": false},
       "T+7": {"action": "Follow up with Manager/Director", "persona": "Manager/Director", "done": false},
       "T+14": {"action": "Value-add to Sr IC/Manager", "persona": "Sr IC/Manager", "done": false}
     },
     "personas": [messages from SHOOT section 13],
     "active": true
   }

3. SIGNAL pipeline-tracker: set next_action = "Networking: T+0 submit"

4. DISPLAY: "Networking cadence started for [company]. Say LINKEDIN CONNECT to send."
```

---

## Execution: On Every Response (Auto-Footer Check)

```
1. READ data/networking_log.json
2. For each active cadence:
   → Calculate T+ = today - submitted_date
   → Check which actions are due (T+ >= action day AND not done)
   → If action due today: set DUE TODAY
   → If action due in future: set as upcoming
3. DISPLAY in AUTO-NETWORKING footer:
```
```
╔═══════════════════════════════════════════════════════╗
║  📡 AUTO-NETWORKING                                    ║
║  🎯 T+0: Submit [company] — due today                  ║
║  ⏳ T+3: Connect IC at [company]                       ║
║  ⏳ T+7: Follow-up Mgr at [company]                    ║
  ║  Say LINKEDIN CONNECT [name] to send, or SKIP.        ║
╚═══════════════════════════════════════════════════════╝

4. **NEW — career-ops enhanced cadence**: ALSO run after every CADENCE command:
   ```bash
   node lib/career-ops/followup-cadence.mjs --summary
   ```
   → Shows overdue/urgent/waiting/cold buckets in dashboard format
   → Detects companies that replied (urgent — respond 24h)
   → Detects 2+ follow-ups with no reply (cold — suggest closing)
   → Merges with existing T+0/T+3/T+7/T+14/T+28 cadence data
```

---

## Execution: On LINKEDIN CONNECT (Action Completed)

```
1. RECEIVE: LINKEDIN CONNECT [persona_name] for [company]
2. READ data/networking_log.json → find matching cadence
3. Mark action as done: "T+3": {"action": "...", "done": true, "sent_date": "YYYY-MM-DD"}
4. UPDATE pipeline PIPELINE.md: next_action = "Waiting for response"
5. DISPLAY: "Sent. Waiting for response. Next: T+7 follow-up."
```

---

## Execution: On SKIP

```
1. RECEIVE: SKIP [company] or SKIP [T+ action]
2. Mark action as skipped in networking_log.json
3. Advance to next action in cadence
```

---

## Commands

| Command | Execution |
|---------|-----------|
| (auto) YES | Triggers cadence start — no SUBMITTED needed |
| `LINKEDIN CONNECT [name] for [company]` | Sends message, marks action done |
| `SKIP [company]` | Skips current action, advances cadence |
| `NETSTAT` | Read `data/networking_log.json` → display full cadence table |
| `SUBMITDATE [company] YYYY-MM-DD` | Override submission date (recalculates all T+ dates) |
| `CADENCE --dashboard` | Enhanced: show overdue/urgent/waiting/cold buckets via followup-cadence.mjs |
| `CADENCE DRAFT [company]` | Generate follow-up email with company-specific context |
| `CADENCE RECORD [company]` | Record a follow-up you actually sent |
| `CADENCE PIN [company] [date]` | Pin specific next-follow-up date |

---

## Hard Rules

1. Cadence auto-starts on YES — never needs SUBMITTED command
2. Footer auto-updates every response — never stale
3. If persona responds → mark "engaged", stop messaging that persona
4. If no response after T+7 of their last message → switch to next persona
5. Never double-message a non-responsive connection
6. If all messages sent → "✅ [Company] cadence complete — waiting for response"
7. If company at T+0 and not yet submitted → footer says "Submit [company] first"
