"""
Reddit & Community Intelligence Synthesizer
Part of the DAEMON skill — ABHIMANYU 2.0 Autonomic System
Scrapes Reddit and other community sources for real-time intelligence
about target companies, industries, roles, and hiring trends.
Synthesizes findings with existing DNA data for enriched outputs.
"""

import json, os, re, time
from datetime import datetime, timezone
from typing import Optional
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
DAEMON_DIR = os.path.join(DATA_DIR, "daemon")
REDDIT_CACHE_DIR = os.path.join(DAEMON_DIR, "reddit_cache")
EVOLUTION_FILE = os.path.join(DAEMON_DIR, "evolution.json")

DEFAULT_SUBREDDITS = [
    "consulting", "cscareerquestions", "jobs", "Vancouver",
    "big4", "sales", "startups", "careerguidance",
    "recruiting", "interviewprep", "salary",
]

COMPANY_SUBREDDITS = {
    "deloitte": ["deloitte", "big4"], "kpmg": ["kpmg", "big4"],
    "ey": ["ey", "big4"], "pwc": ["pwc", "big4"],
    "mckinsey": ["consulting"], "bain": ["consulting"], "bcg": ["consulting"],
    "shopify": ["shopify"], "amazon": ["amazon"], "telus": ["telus"],
    "lululemon": ["lululemon"],
}

def ensure_dirs():
    for d in [DAEMON_DIR, REDDIT_CACHE_DIR]:
        os.makedirs(d, exist_ok=True)

def load_evolution():
    ensure_dirs()
    if os.path.exists(EVOLUTION_FILE):
        with open(EVOLUTION_FILE) as f:
            return json.load(f)
    return {
        "signal_weights": {
            "reddit_salary": 0.6, "reddit_culture": 0.5,
            "reddit_interview": 0.8, "glassdoor_trend": 0.7,
            "company_subreddit": 0.9, "industry_trend": 0.5,
        },
        "winning_signals": [], "losing_signals": [],
        "adjustments": [],
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }

def save_evolution(evolution):
    ensure_dirs()
    evolution["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(EVOLUTION_FILE, "w") as f:
        json.dump(evolution, f, indent=2)

def scrape_reddit(subreddit, query="", limit=5):
    if not HAS_REQUESTS:
        return [{"source": "mock", "subreddit": subreddit,
                 "title": "Requests library not available",
                 "body": "Install requests for live Reddit scraping",
                 "relevance": 0}]
    try:
        headers = {"User-Agent": "ABHIMANYU-DAEMON/2.0"}
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        params = {"q": query, "restrict_sr": "on", "sort": "new",
                  "limit": limit, "t": "month"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json()
        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "source": "reddit", "subreddit": subreddit,
                "title": post.get("title", ""),
                "body": (post.get("selftext", "") or "")[:500],
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "created_utc": post.get("created_utc", 0),
                "relevance": 0.5,
            })
            time.sleep(0.5)
        return posts
    except Exception:
        return []

def search_all_company(company, industry=""):
    results = []
    relevant_subs = COMPANY_SUBREDDITS.get(company.lower(), []) + DEFAULT_SUBREDDITS
    relevant_subs = list(set(relevant_subs))
    for sub in relevant_subs[:5]:
        results.extend(scrape_reddit(sub, company, limit=3))
        if industry and industry.lower() != company.lower():
            results.extend(scrape_reddit(sub, industry, limit=2))
        time.sleep(0.5)
    results.sort(key=lambda x: (x.get("score", 0) + x.get("num_comments", 0)), reverse=True)
    for i, r in enumerate(results):
        r["relevance"] = max(0, 1.0 - (i * 0.1))
    return results[:15]

def synthesize_company_intel(company, industry="", existing_dna=None):
    ensure_dirs()
    evolution = load_evolution()
    cache_file = os.path.join(
        REDDIT_CACHE_DIR,
        f"{company.lower().replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d')}.json"
    )
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            cached = json.load(f)
            if time.time() - cached.get("cached_at", 0) < 86400:
                return cached
    raw_posts = search_all_company(company, industry)
    signals = {"salary_signals": [], "culture_signals": [],
               "interview_signals": [], "hiring_trends": [],
               "red_flags": [], "green_flags": []}
    for post in raw_posts:
        text = f"{post.get('title', '')} {post.get('body', '')}".lower()
        sub = post.get("subreddit", "")
        sals = re.findall(r'\$(\d{2,3})[kK]', text)
        if sals or any(w in text for w in ["salary", "compensation", "pay", "offer"]):
            signals["salary_signals"].append({
                "source": f"r/{sub}", "title": post.get("title"),
                "url": post.get("url"), "data": sals[:3] if sals else "mentioned",
                "relevance": evolution["signal_weights"].get("reddit_salary", 0.6),
            })
        if any(w in text for w in ["interview", "case study", "superday", "assessment", "hiring process"]):
            signals["interview_signals"].append({
                "source": f"r/{sub}", "title": post.get("title"),
                "url": post.get("url"), "data": (post.get("body") or "")[:300],
                "relevance": evolution["signal_weights"].get("reddit_interview", 0.8),
            })
        if any(w in text for w in ["culture", "wlb", "work life", "hours", "toxic"]):
            signals["culture_signals"].append({
                "source": f"r/{sub}", "title": post.get("title"),
                "url": post.get("url"), "data": (post.get("body") or "")[:300],
                "relevance": evolution["signal_weights"].get("reddit_culture", 0.5),
            })
        if any(w in text for w in ["layoff", "firing", "pivot", "restructuring", "exodus"]):
            signals["red_flags"].append({
                "source": f"r/{sub}", "title": post.get("title"),
                "url": post.get("url"), "signal": (post.get("body") or "")[:200],
            })
        if any(w in text for w in ["hiring", "growth", "promotion", "great culture", "bonus", "ipo"]):
            signals["green_flags"].append({
                "source": f"r/{sub}", "title": post.get("title"),
                "url": post.get("url"), "signal": (post.get("body") or "")[:200],
            })
    synthesis = {
        "company": company, "industry": industry,
        "scraped_at": time.time(), "cached_at": time.time(),
        "total_posts_analyzed": len(raw_posts),
        "signals": signals,
        "summary": _generate_summary(signals, evolution),
        "actionable_insights": _generate_insights(signals, company),
        "source_urls": list(set(p.get("url") for p in raw_posts if p.get("url"))),
    }
    with open(cache_file, "w") as f:
        json.dump(synthesis, f, indent=2)
    return synthesis

def _generate_summary(signals, evolution):
    parts = []
    if signals["salary_signals"]:
        parts.append(f"Salary intel found ({len(signals['salary_signals'])} sources)")
    if signals["interview_signals"]:
        parts.append(f"Interview intel ({len(signals['interview_signals'])} sources)")
    if signals["culture_signals"]:
        parts.append(f"Culture signals ({len(signals['culture_signals'])} sources)")
    if signals["red_flags"]:
        parts.append(f"{len(signals['red_flags'])} red flag(s)")
    if signals["green_flags"]:
        parts.append(f"{len(signals['green_flags'])} green flag(s)")
    weights = evolution.get("signal_weights", {})
    avg_w = sum(weights.values()) / len(weights) if weights else 0.5
    conf = min(1.0, (len(signals["salary_signals"]) * 0.1 +
                      len(signals["interview_signals"]) * 0.15 +
                      len(signals["culture_signals"]) * 0.05) * avg_w)
    if conf > 0.3:
        parts.append(f"Confidence: {conf:.0%}")
    else:
        parts.append("Limited community data - relying on DNA analysis")
    return " | ".join(parts) if parts else "No community signals found"

def _generate_insights(signals, company):
    insights = []
    if signals["salary_signals"]:
        sals = []
        for s in signals["salary_signals"]:
            if isinstance(s.get("data"), list):
                sals.extend(s["data"])
        if sals:
            insights.append(f"Community salary range: ${min(int(v) for v in sals)}K-${max(int(v) for v in sals)}K")
    if signals["interview_signals"]:
        insights.append(f"Interview insight: {signals['interview_signals'][0].get('data', '')[:100]}...")
    if signals["red_flags"]:
        insights.append(f"Caution: {signals['red_flags'][0].get('signal', '')[:100]}...")
    if signals["green_flags"]:
        insights.append(f"Positive: {signals['green_flags'][0].get('signal', '')[:100]}...")
    return insights

def record_outcome(company, outcome, signals_used):
    evolution = load_evolution()
    entry = {"company": company, "outcome": outcome,
             "signals_used": signals_used,
             "timestamp": datetime.now(timezone.utc).isoformat()}
    if outcome in ["offer", "callback"]:
        evolution["winning_signals"].append(entry)
        for sig in signals_used:
            k = f"reddit_{sig.replace(' ', '_')}"
            if k in evolution["signal_weights"]:
                evolution["signal_weights"][k] = min(1.0, evolution["signal_weights"][k] + 0.1)
    elif outcome in ["rejection", "ghosted"]:
        evolution["losing_signals"].append(entry)
        for sig in signals_used:
            k = f"reddit_{sig.replace(' ', '_')}"
            if k in evolution["signal_weights"]:
                evolution["signal_weights"][k] = max(0.0, evolution["signal_weights"][k] - 0.05)
    evolution["adjustments"].append({
        "action": "weight_update", "trigger": outcome,
        "company": company,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    save_evolution(evolution)

if __name__ == "__main__":
    import sys
    company = sys.argv[1] if len(sys.argv) > 1 else "Deloitte"
    industry = sys.argv[2] if len(sys.argv) > 2 else "consulting"
    result = synthesize_company_intel(company, industry)
    print(json.dumps(result, indent=2))
