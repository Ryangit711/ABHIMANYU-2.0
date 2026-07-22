#!/usr/bin/env python3
"""
APIFY_FETCH.py — Apify-powered job scraper for ABHIMANYU system
Constitutional Amendment #13: Apify integration layer

Fills 2 gaps that webfetch/websearch can't:
  1. JS-heavy career portals (Lever, Ashby, Workday) → apify_fetch(url) renders full DOM
  2. Bulk job search across multiple sources → apify_search_jobs(query) returns structured listings

Usage:
  python3 APIFY_FETCH.py fetch <url>         # Render a JS-heavy URL, return clean text
  python3 APIFY_FETCH.py search <query>      # Search jobs across sources
  python3 APIFY_FETCH.py test                # Test API key is valid
"""

import json
import os
import sys
import time
from typing import Optional

import requests

SECRETS_PATH = "secrets.json"
APIFY_BASE = "https://api.apify.com/v2"

# Puppeteer Web Scraper — renders JS-heavy pages (needs one-time approval at URL below)
WEB_SCRAPER_ACTOR = "moJRLRc85AitArpNN"
WEB_SCRAPER_APPROVAL_URL = "https://console.apify.com/actors/moJRLRc85AitArpNN?approvePermissions=true"

# Job search via Apify — run a search using Google Jobs index (install from Apify Store first)
# Search Apify Store for "Google Jobs Scraper" by drobnikj, install to your account, then set ID here
JOBS_SCRAPER_ACTOR = None  # Set after installing from store.apify.com


def load_api_key() -> Optional[str]:
    if not os.path.exists(SECRETS_PATH):
        return None
    with open(SECRETS_PATH) as f:
        data = json.load(f)
        return data.get("apify_api_key")


def _check_key():
    key = load_api_key()
    if not key:
        print("ERROR: No Apify API key found in secrets.json")
        print("       Create secrets.json with: {\"apify_api_key\": \"your_key\"}")
        sys.exit(1)
    return key


def _wait_for_run(actor_id: str, run_id: str, token: str, poll_interval: int = 3, timeout: int = 120) -> dict:
    """Poll Apify run until finished, return dataset items."""
    url = f"{APIFY_BASE}/acts/{actor_id}/runs/{run_id}?token={token}"
    elapsed = 0
    while elapsed < timeout:
        r = requests.get(url)
        if r.status_code != 200:
            return {"error": f"Run status failed: {r.status_code} {r.text}"}
        data = r.json().get("data", {})
        status = data.get("status", "UNKNOWN")
        if status == "SUCCEEDED":
            ds_id = data.get("defaultDatasetId")
            if not ds_id:
                return {"error": "No defaultDatasetId in run data"}
            items_url = f"{APIFY_BASE}/datasets/{ds_id}/items?token={token}&format=json"
            items_r = requests.get(items_url)
            if items_r.status_code != 200:
                return {"error": f"Items fetch failed: {items_r.status_code}"}
            return {"items": items_r.json()}
        elif status in ("FAILED", "TIMED-OUT", "ABORTED"):
            return {"error": f"Run {status}: {data.get('statusMessage', '')}"}
        time.sleep(poll_interval)
        elapsed += poll_interval
    return {"error": "Timeout waiting for Apify run"}


def apify_fetch(url: str) -> str:
    """
    Render a JS-heavy URL via Apify Web Scraper and return clean page text.
    Fallback for Lever/Ashby/Workday career pages that webfetch can't handle.
    """
    token = _check_key()
    run_input = {
        "startUrls": [{"url": url}],
        "pageFunction": (
            "async function pageFunction(context) {"
            "  const { request, $ } = context;"
            "  const text = $('body').text().replace(/\\s+/g, ' ').trim();"
            "  return { url: request.url, title: $('title').text().trim(), text: text.substring(0, 50000) };"
            "}"
        ),
        "proxyConfiguration": {"useApifyProxy": True},
    }
    run_url = f"{APIFY_BASE}/acts/{WEB_SCRAPER_ACTOR}/runs?token={token}"
    r = requests.post(run_url, json=run_input)
    if r.status_code == 403:
        return (
            f"⚠️ Apify Web Scraper needs one-time permission approval.\n"
            f"   Open this URL in your browser and approve:\n"
            f"   {WEB_SCRAPER_APPROVAL_URL}\n"
            f"   Then re-run this command. (Only needed once.)"
        )
    if r.status_code not in (200, 201):
        return f"ERROR: Apify run start failed: {r.status_code} {r.text}"
    run_id = r.json().get("data", {}).get("id")
    if not run_id:
        return f"ERROR: No run ID in response: {r.text}"
    result = _wait_for_run(WEB_SCRAPER_ACTOR, run_id, token)
    if "error" in result:
        return f"ERROR: {result['error']}"
    items = result.get("items", [])
    if not items:
        return "ERROR: No items returned from Apify scraper"
    return items[0].get("text", "ERROR: No text in response")


def apify_search_jobs(query: str, location: str = "Canada", max_results: int = 30) -> list:
    """
    Search jobs via Apify (requires a jobs scraper actor installed from Apify Store).
    Until installed, returns a helpful message pointing to the Store.
    """
    if not JOBS_SCRAPER_ACTOR:
        return [{"info": "No jobs scraper actor configured.",
                  "action": "Go to https://apify.com/store, search 'Google Jobs Scraper', install it,"
                            " then set JOBS_SCRAPER_ACTOR in APIFY_FETCH.py to its ID."}]
    token = _check_key()
    run_input = {
        "query": f"{query} {location}",
        "maxPages": 3,
        "resultsPerPage": max_results,
    }
    run_url = f"{APIFY_BASE}/acts/{JOBS_SCRAPER_ACTOR}/runs?token={token}"
    r = requests.post(run_url, json=run_input)
    if r.status_code not in (200, 201):
        return [{"error": f"Job search run start failed: {r.status_code} {r.text}"}]
    run_id = r.json().get("data", {}).get("id")
    if not run_id:
        return [{"error": f"No run ID: {r.text}"}]
    result = _wait_for_run(JOBS_SCRAPER_ACTOR, run_id, token)
    if "error" in result:
        return [{"error": result["error"]}]
    items = result.get("items", [])
    parsed = []
    for item in items:
        parsed.append({
            "title": item.get("title", ""),
            "company": item.get("companyName", item.get("company", "")),
            "location": item.get("location", ""),
            "salary": item.get("salary", item.get("salaryRange", "")),
            "url": item.get("url", item.get("link", "")),
            "source": item.get("source", "google_jobs"),
        })
    return parsed


def test_key() -> str:
    """Test that the API key is valid by calling Apify user info."""
    token = _check_key()
    url = f"{APIFY_BASE}/users/me?token={token}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json().get("data", {})
        email = data.get("email", "unknown")
        plan_name = data.get("plan", {})
        if isinstance(plan_name, dict):
            plan_name = plan_name.get("tier", plan_name.get("id", "unknown"))
        proxy_avail = data.get("proxy", {})
        usage = data.get("usage", {})
        usage_credits = usage.get("monthlyUsageCreditsUsd", usage.get("monthlyBasePriceUsd", 0))
        return (
            f"✅ Apify API key valid\n"
            f"   Account: {email}\n"
            f"   Plan: {plan_name} (${usage_credits}/mo credits)\n"
            f"   JS rendering: {'⚠️ Needs approval → ' + WEB_SCRAPER_APPROVAL_URL if True else '✅ Ready'}"
        )
    else:
        return f"❌ Apify API key invalid: {r.status_code} {r.text}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 APIFY_FETCH.py fetch <url>         # Render JS page")
        print("  python3 APIFY_FETCH.py search <query>      # Search jobs")
        print("  python3 APIFY_FETCH.py test                # Test API key")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "fetch":
        if len(sys.argv) < 3:
            print("Usage: python3 APIFY_FETCH.py fetch <url>")
            sys.exit(1)
        result = apify_fetch(sys.argv[2])
        print(result[:10000] if len(result) > 10000 else result)

    elif cmd == "search":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "operations manager"
        results = apify_search_jobs(query)
        print(json.dumps(results, indent=2))

    elif cmd == "test":
        print(test_key())

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
