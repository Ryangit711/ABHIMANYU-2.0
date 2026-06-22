"""
Social Intelligence Layer — DAEMON Enhancement
ABHIMANYU 2.0

Handles Instagram (captions + reel transcription) and X.com intelligence.
Cross-references against existing system knowledge before assimilating.
"""

import json, os, re, time, tempfile
from datetime import datetime, timezone

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
DAEMON_DIR = os.path.join(DATA_DIR, "daemon")
SOCIAL_CACHE_DIR = os.path.join(DAEMON_DIR, "social_cache")
ASSIMILATED_DIR = os.path.join(DAEMON_DIR, "assimilated")
EVOLUTION_FILE = os.path.join(DAEMON_DIR, "evolution.json")

# Paths to existing system knowledge for cross-reference
LEARNED_DIR = os.path.join(DATA_DIR, "learned")
FIT_MAPS_DIR = os.path.join(DATA_DIR, "fit_maps")
THOUGHT_LOG_DIR = os.path.join(DATA_DIR, "thought_log")
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..")


def ensure_dirs():
    for d in [DAEMON_DIR, SOCIAL_CACHE_DIR, ASSIMILATED_DIR]:
        os.makedirs(d, exist_ok=True)


def load_evolution():
    ensure_dirs()
    if os.path.exists(EVOLUTION_FILE):
        with open(EVOLUTION_FILE) as f:
            return json.load(f)
    return {"signal_weights": {}, "winning_signals": [], "losing_signals": [], "adjustments": []}


def save_evolution(ev):
    ensure_dirs()
    ev["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(EVOLUTION_FILE, "w") as f:
        json.dump(ev, f, indent=2)


def load_existing_knowledge() -> dict:
    """Load all existing system knowledge for cross-referencing."""
    knowledge = {
        "learned_companies": set(),
        "learned_keywords": set(),
        "learned_pipes": {},
        "fit_map_companies": set(),
        "skill_names": set(),
        "known_concepts": set(),
    }

    # Learned files
    if os.path.exists(LEARNED_DIR):
        for f in os.listdir(LEARNED_DIR):
            if f.endswith(".md"):
                knowledge["learned_companies"].add(f.replace(".md", ""))
                fpath = os.path.join(LEARNED_DIR, f)
                try:
                    with open(fpath) as fh:
                        content = fh.read().lower()
                        words = set(re.findall(r'\b[a-z]{4,}\b', content))
                        knowledge["known_concepts"].update(words)
                except:
                    pass

    # Fit maps
    if os.path.exists(FIT_MAPS_DIR):
        for f in os.listdir(FIT_MAPS_DIR):
            if f.endswith(".md") and f != "INDEX.md":
                knowledge["fit_map_companies"].add(f.replace(".md", "").upper())

    # Keywords
    kw_file = os.path.join(LEARNED_DIR, "keywords.md")
    if os.path.exists(kw_file):
        with open(kw_file) as f:
            knowledge["known_concepts"].add(f.read().lower())

    # Skill names
    if os.path.exists(SKILLS_DIR):
        for d in os.listdir(SKILLS_DIR):
            if os.path.isdir(os.path.join(SKILLS_DIR, d)):
                knowledge["skill_names"].add(d.lower())

    return knowledge


def is_already_known(text: str, knowledge: dict) -> dict:
    """Check if content is already in the system. Returns what's new vs known."""
    text_lower = text.lower()
    found_concepts = set()
    new_concepts = set()

    # Check against known concepts
    for concept in knowledge["known_concepts"]:
        if isinstance(concept, str) and concept in text_lower:
            found_concepts.add(concept)

    # Check against company names
    mentioned_companies = []
    for company in knowledge["fit_map_companies"]:
        if company.lower() in text_lower:
            mentioned_companies.append(company)

    # Check against learned companies
    for company in knowledge["learned_companies"]:
        if company.lower() in text_lower and company.upper() not in mentioned_companies:
            mentioned_companies.append(company.upper())

    # Extract potential new concepts (capitalized phrases, unique terms)
    potential_new = set(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text))
    for pn in potential_new:
        if pn.lower() not in knowledge["known_concepts"]:
            new_concepts.add(pn)

    return {
        "is_fully_known": len(new_concepts) == 0 and len(mentioned_companies) <= 1,
        "found_concepts_count": len(found_concepts),
        "mentioned_companies": mentioned_companies,
        "new_concepts": list(new_concepts)[:10],
        "novelty_score": min(1.0, len(new_concepts) / 20),
    }


def fetch_instagram_post(url: str) -> dict:
    """Scrape public Instagram post for caption and metadata."""
    result = {
        "source": "instagram",
        "url": url,
        "caption": "",
        "has_video": False,
        "transcription": None,
        "extracted_at": time.time(),
        "error": None,
    }

    if not HAS_REQUESTS:
        result["error"] = "requests library required"
        return result

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120.0.6099.230 Mobile Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=15)

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        html = resp.text

        # Extract caption from meta tags or embedded JSON
        # Instagram embeds data in <script type="application/ld+json"> or meta tags
        caption_match = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', html)
        if caption_match:
            result["caption"] = caption_match.group(1)

        # Also try JSON embedded data
        json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', html, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1))
                # Navigate the Instagram state tree - structure varies
                items = data.get("items", {})
                for key in items:
                    item = items[key]
                    if isinstance(item, dict):
                        cap = item.get("caption", "")
                        if isinstance(cap, dict):
                            result["caption"] = cap.get("text", result["caption"])
                        elif isinstance(cap, str) and cap:
                            result["caption"] = cap
                        result["has_video"] = item.get("media_type") == 2 or item.get("is_video", False)
            except (json.JSONDecodeError, AttributeError):
                pass

        # Fallback: extract from page title
        if not result["caption"]:
            title_match = re.search(r'<title>([^<]+)</title>', html)
            if title_match:
                result["caption"] = title_match.group(1)

        # Clean caption
        result["caption"] = result["caption"].strip()[:2000]

        # Note about transcription
        if result["has_video"]:
            result["transcription"] = None
            result["transcription_note"] = "Video/reel detected. Transcription requires audio download + speech-to-text (whisper). Manual transcription or API key needed for full automation. Caption extracted above."

    except Exception as e:
        result["error"] = str(e)

    return result


def fetch_x_post(url: str) -> dict:
    """Scrape public X.com (Twitter) post for text content."""
    result = {
        "source": "x.com",
        "url": url,
        "text": "",
        "author": "",
        "extracted_at": time.time(),
        "error": None,
    }

    if not HAS_REQUESTS:
        result["error"] = "requests library required"
        return result

    try:
        # Convert x.com to twitter.com if needed
        api_url = url.replace("x.com", "twitter.com")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.6099.230 Safari/537.36"
        }
        resp = requests.get(api_url, headers=headers, timeout=15)

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        html = resp.text

        # Extract tweet text from meta tags
        desc_match = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', html)
        if desc_match:
            result["text"] = desc_match.group(1)

        # Try to get author
        author_match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html)
        if author_match:
            title = author_match.group(1)
            # Usually "Name on X: tweet text" or similar
            result["author"] = title.split(" on X")[0] if " on X" in title else title

        # Clean
        result["text"] = result["text"].strip()[:2000]

    except Exception as e:
        result["error"] = str(e)

    return result


def ingest_social_post(url: str, platform: str = "auto") -> dict:
    """
    Main entry point. Takes a URL, fetches content, cross-references
    against existing knowledge, and returns analysis with assimilation recommendation.
    """
    ensure_dirs()
    knowledge = load_existing_knowledge()

    # Auto-detect platform
    if platform == "auto":
        if "instagram.com" in url.lower():
            platform = "instagram"
        elif "x.com" in url.lower() or "twitter.com" in url.lower():
            platform = "x.com"
        else:
            return {"error": f"Unsupported platform. URL must be Instagram or X.com. Got: {url}"}

    # Fetch content
    if platform == "instagram":
        content = fetch_instagram_post(url)
    elif platform == "x.com":
        content = fetch_x_post(url)
    else:
        return {"error": f"Unknown platform: {platform}"}

    if content.get("error"):
        return content

    # Extract text for analysis
    text_to_analyze = content.get("caption") or content.get("text") or ""
    if not text_to_analyze:
        content["analysis"] = {"error": "No text content extracted"}
        return content

    # Cross-reference with existing knowledge
    analysis = is_already_known(text_to_analyze, knowledge)

    # Generate insight
    content["analysis"] = analysis
    content["already_in_system"] = analysis["is_fully_known"]

    if analysis["is_fully_known"]:
        content["recommendation"] = "SKIP — already in system"
        content["justification"] = "All concepts and signals already present in learned data, fit maps, or skill definitions."
    else:
        content["recommendation"] = "ASSIMILATE"
        content["justification"] = f"New concepts found: {', '.join(analysis['new_concepts'][:5]) or 'novel combination of known signals'}. Mentions companies: {', '.join(analysis['mentioned_companies']) or 'none'}."

    # Cache it
    cache_key = re.sub(r'[^a-zA-Z0-9]', '_', url.split("?")[0])[:80]
    cache_file = os.path.join(SOCIAL_CACHE_DIR, f"{cache_key}.json")
    with open(cache_file, "w") as f:
        json.dump(content, f, indent=2)

    return content


def assimilate(content: dict) -> dict:
    """
    Assimilate new intelligence into the system.
    Writes to data/daemon/assimilated/ for review before committing to main system.
    """
    ensure_dirs()
    text = content.get("caption") or content.get("text") or ""
    analysis = content.get("analysis", {})
    source = content.get("source", "unknown")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', text[:50])[:40]

    assimilated = {
        "assimilated_at": timestamp,
        "source": source,
        "source_url": content.get("url"),
        "original_text": text[:1000],
        "novelty_score": analysis.get("novelty_score", 0.5),
        "new_concepts": analysis.get("new_concepts", []),
        "mentioned_companies": analysis.get("mentioned_companies", []),
        "status": "pending_review",
        "note": "Review this before committing to learned/ or fit_maps/",
    }

    # Write to assimilated queue
    out_file = os.path.join(ASSIMILATED_DIR, f"{timestamp[:10]}_{slug}.json")
    with open(out_file, "w") as f:
        json.dump(assimilated, f, indent=2)

    # Also log to evolution
    ev = load_evolution()
    ev.setdefault("assimilations", [])
    ev["assimilations"].append({
        "timestamp": timestamp,
        "source": source,
        "new_concepts_count": len(analysis.get("new_concepts", [])),
        "novelty_score": analysis.get("novelty_score", 0),
    })
    save_evolution(ev)

    return assimilated


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python social_intelligence_layer.py <url> [--assimilate]")
        print("  <url>        Instagram or X.com post URL")
        print("  --assimilate  Also write to assimilation queue")
        sys.exit(1)

    url = sys.argv[1]
    should_assimilate = "--assimilate" in sys.argv

    result = ingest_social_post(url)
    print(json.dumps(result, indent=2, default=str))

    if should_assimilate and not result.get("already_in_system"):
        ass = assimilate(result)
        print(f"\nAssimilated: {ass['status']} -> {ass.get('assimilated_at')}")
