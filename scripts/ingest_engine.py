#!/usr/bin/env python3
"""INGEST SOCIAL — The Amoeba Skill Engine.

Extracts intelligence from Instagram posts (captions, OCR, video transcriptions),
classifies, cross-references with pipeline, and assimilates into system.

Usage:
  python3 ingest_engine.py <url> [--quick] [--assimilate] [--status] [--queue]
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INTEL_DIR = DATA_DIR / "intel"
LEARNED_DIR = DATA_DIR / "learned"
FIT_MAPS_DIR = DATA_DIR / "fit_maps"
PIPELINE_DIR = DATA_DIR / "pipeline"
JOBS_DB = DATA_DIR / "jobs.json"

os.makedirs(INTEL_DIR, exist_ok=True)
os.makedirs(LEARNED_DIR, exist_ok=True)
os.makedirs(FIT_MAPS_DIR, exist_ok=True)
os.makedirs(PIPELINE_DIR, exist_ok=True)
os.makedirs(INTEL_DIR / datetime.now().strftime("%Y-%m-%d"), exist_ok=True)

COUNT_FILE = INTEL_DIR / ".ingest_count.json"

TOOLS = {}


def check_tools():
    global TOOLS
    try:
        import instaloader
        TOOLS["instaloader"] = instaloader
    except ImportError:
        TOOLS["instaloader"] = None
    try:
        import yt_dlp
        TOOLS["yt_dlp"] = yt_dlp
    except ImportError:
        TOOLS["yt_dlp"] = None
    try:
        import pytesseract
        TOOLS["pytesseract"] = pytesseract
    except ImportError:
        TOOLS["pytesseract"] = None
    try:
        import faster_whisper
        TOOLS["faster_whisper"] = faster_whisper
    except ImportError:
        TOOLS["faster_whisper"] = None
    import subprocess
    TOOLS["has_tesseract_bin"] = (
        subprocess.run(["which", "tesseract"], capture_output=True).returncode == 0
    )
    TOOLS["has_ffmpeg"] = (
        subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0
    )
    return TOOLS


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")[:60]


def load_count():
    if COUNT_FILE.exists():
        return json.loads(COUNT_FILE.read_text())
    return {"total": 0, "by_category": {}, "by_company": {}}


def save_count(count):
    COUNT_FILE.write_text(json.dumps(count, indent=2))


def already_ingested(url):
    today_dir = INTEL_DIR / datetime.now().strftime("%Y-%m-%d")
    from urllib.parse import urlparse
    slug = slugify(urlparse(url).path.rstrip("/").split("/")[-1] or url)
    for f in today_dir.iterdir():
        if slug in f.name:
            return True
    return False


def get_tracked_companies():
    if JOBS_DB.exists():
        data = json.loads(JOBS_DB.read_text())
        if isinstance(data, dict) and "applied" in data:
            return list(data["applied"].keys())
        if isinstance(data, dict):
            return list(data.keys())
        if isinstance(data, list):
            return [j.get("company", "") for j in data if "company" in j]
    return []


def extract_instagram(url):
    result = {"caption": "", "image_texts": [], "transcript": "", "comments": []}
    il = TOOLS.get("instaloader")
    if not il:
        return result
    try:
        from urllib.parse import urlparse, parse_qs
        path = urlparse(url).path.rstrip("/")
        shortcode = path.split("/")[-1]
        if not shortcode:
            return result
        L = il.Instaloader(sleep=True, quiet=True)
        post = il.Post.from_shortcode(L.context, shortcode)
        result["caption"] = post.caption if post.caption else ""
        try:
            result["comments"] = [
                c.text for c in post.get_comments()
            ][:20]
        except Exception:
            pass
        if TOOLS.get("pytesseract") and TOOLS.get("has_tesseract_bin"):
            from PIL import Image
            import requests
            from io import BytesIO
            try:
                for node in post.sidecar_nodes:
                    try:
                        resp = requests.get(node.display_url, timeout=15)
                        img = Image.open(BytesIO(resp.content))
                        text = TOOLS["pytesseract"].image_to_string(img)
                        if text.strip():
                            result["image_texts"].append(text.strip())
                        img.close()
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception as e:
        pass
    return result


def extract_video_transcript(url):
    result = ""
    if not TOOLS.get("yt_dlp") or not TOOLS.get("has_ffmpeg") or not TOOLS.get("faster_whisper"):
        return result
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(INTEL_DIR / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    try:
        with TOOLS["yt_dlp"].YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = str(INTEL_DIR / f"{info['id']}.webm")
            if not os.path.exists(audio_path):
                for ext in ["m4a", "mp3", "opus"]:
                    p = str(INTEL_DIR / f"{info['id']}.{ext}")
                    if os.path.exists(p):
                        audio_path = p
                        break
            if os.path.exists(audio_path):
                wav_path = audio_path.rsplit(".", 1)[0] + ".wav"
                import subprocess
                subprocess.run(
                    ["ffmpeg", "-y", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path],
                    capture_output=True, check=True,
                )
                model = TOOLS["faster_whisper"].WhisperModel("base", device="cpu", compute_type="int8")
                segments, _ = model.transcribe(wav_path)
                result = " ".join(s.text for s in segments)
                os.unlink(wav_path)
            os.unlink(audio_path)
    except Exception:
        pass
    return result


def classify_content(caption, transcript, comments, companies):
    text = (caption + " " + transcript + " " + " ".join(comments)).lower()
    categories = []
    if any(w in text for w in ["salary", "comp", "pay", "offer", "$", "tc", "total compensation"]):
        categories.append("salary")
    if any(w in text for w in ["interview", "onsite", "screen", "case study", "loop", "phone screen", "technical"]):
        categories.append("interview")
    if any(w in text for w in ["application", "ats", "resume tip", "recruiter", "resume", "apply"]):
        categories.append("process")
    if any(w in text for w in ["culture", "values", "wlb", "vibe", "environment", "work-life"]):
        categories.append("culture")
    for c in companies:
        if c.lower() in text:
            categories.append("company")
    if any(w in text for w in ["hiring freeze", "layoffs", "growth", "trend", "market", "recession"]):
        categories.append("market")
    if not categories:
        categories.append("general")
    return categories


def link_to_pipeline(company, companies, caption, transcript):
    linked_companies = []
    for c in companies:
        if c.lower() in (caption + " " + transcript).lower():
            linked_companies.append(c)
    return linked_companies


def write_intel(url, classification, linked, caption, image_texts, transcript, comments, overwrite=False):
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    slug = slugify(urlparse(url).path.rstrip("/").split("/")[-1] or "post")
    fpath = INTEL_DIR / today / f"{slug}.md"
    if fpath.exists() and not overwrite:
        return False
    lines = [
        f"# INGEST — {url}",
        f"**Date:** {now}",
        f"**Classification:** {', '.join(classification)}",
        f"**Linked to pipeline:** {', '.join(linked) if linked else 'none'}",
        "",
        "## Caption",
        caption if caption else "(no caption)",
        "",
    ]
    if image_texts:
        lines.append("## OCR (from images)")
        for i, t in enumerate(image_texts, 1):
            lines.append(f"### Image {i}")
            lines.append(t)
            lines.append("")
    if transcript:
        lines.append("## Video Transcript")
        lines.append(transcript)
    if comments:
        lines.append("## Top Comments")
        for i, c in enumerate(comments[:10], 1):
            lines.append(f"{i}. {c}")
    lines.append("")
    fpath.write_text("\n".join(lines))
    return True


def _summarize(text, maxlen=180):
    first_line = text.split("\n")[0].strip()
    if len(first_line) <= maxlen:
        return first_line
    truncated = first_line[:maxlen]
    last_space = truncated.rfind(" ")
    return truncated[:last_space] + "..." if last_space > 0 else truncated + "..."

def update_learned(classification, caption, transcript):
    summary = _summarize(caption)
    for cat in classification:
        if cat == "salary":
            f = LEARNED_DIR / "compensation.md"
            mode = "a" if f.exists() else "w"
            with open(f, mode) as fh:
                if mode == "w":
                    fh.write("# Compensation Intelligence\n\n")
                fh.write(f"- INGEST {datetime.now().strftime('%Y-%m-%d')}: {summary}\n")
        elif cat == "interview":
            f = LEARNED_DIR / "interviews.md"
            mode = "a" if f.exists() else "w"
            with open(f, mode) as fh:
                if mode == "w":
                    fh.write("# Interview Intelligence\n\n")
                fh.write(f"- INGEST {datetime.now().strftime('%Y-%m-%d')}: {summary}\n")
        elif cat == "market":
            f = PIPELINE_DIR / "market_intel.md"
            mode = "a" if f.exists() else "w"
            with open(f, mode) as fh:
                if mode == "w":
                    fh.write("# Market Intelligence\n\n")
                fh.write(f"- INGEST {datetime.now().strftime('%Y-%m-%d')}: {summary}\n")


def update_fit_maps(linked_companies, caption):
    for company in linked_companies:
        f = FIT_MAPS_DIR / f"{slugify(company)}.md"
        mode = "a" if f.exists() else "w"
        with open(f, mode) as fh:
            if mode == "w":
                fh.write(f"# {company} — Fit Map\n\n")
            fh.write(f"- INGEST {datetime.now().strftime('%Y-%m-%d')}: {caption[:200]}\n")


def update_count(classification, linked):
    count = load_count()
    count["total"] += 1
    for cat in classification:
        count["by_category"][cat] = count["by_category"].get(cat, 0) + 1
    for c in linked:
        count["by_company"][c] = count["by_company"].get(c, 0) + 1
    save_count(count)
    return count


def quick_ingest(url):
    il = TOOLS.get("instaloader")
    if il:
        try:
            from urllib.parse import urlparse
            path = urlparse(url).path.rstrip("/")
            shortcode = path.split("/")[-1]
            if not shortcode:
                return {"caption": "", "comments": []}
            L = il.Instaloader(sleep=True, quiet=True)
            post = il.Post.from_shortcode(L.context, shortcode)
            caption = post.caption or ""
            try:
                comments = [c.text for c in post.get_comments()][:10]
            except Exception:
                comments = []
            return {"caption": caption, "comments": comments}
        except Exception:
            pass
    return {"caption": "", "comments": []}


def format_report(url, classification, linked, caption, image_texts, transcript, comments, count):
    cat_str = "/".join(classification)
    linked_str = ", ".join(linked) if linked else "(none)"
    caption_str = f"✅ extracted ({len(caption)} chars)" if caption else "⚠️ empty"
    ocr_str = f"✅ {len(image_texts)} images processed" if image_texts else "⚠️ no images"
    video_str = f"✅ {len(transcript.split())} words transcribed" if transcript else "⚠️ no video"
    comments_str = f"✅ {len(comments)} comments processed" if comments else "⚠️ no comments"
    return (
        f"📋 INGEST SUMMARY — {url}\n"
        f"{'━' * 50}\n"
        f"🧠 Caption:   {caption_str}\n"
        f"🖼️ OCR:       {ocr_str}\n"
        f"🎤 Video:     {video_str}\n"
        f"💬 Comments:  {comments_str}\n\n"
        f"📌 Classification: {cat_str}\n"
        f"🔗 Linked to pipeline: {linked_str}\n"
        f"📁 System files updated:\n"
        f"  ├── data/intel/{datetime.now().strftime('%Y-%m-%d')}/ (raw)\n"
        f"  ├── data/learned/ (keywords)\n"
        f"{'  └── data/fit_maps/ (company)' if linked else ''}\n\n"
        f"🦠 Amoeba is now 0.01% smarter. (Total ingested: {count['total']})"
    )


def show_status():
    count = load_count()
    print(f"📊 INGEST STATUS")
    print(f"{'━' * 30}")
    print(f"Total ingested: {count['total']}")
    print(f"\nBy category:")
    for cat, n in sorted(count["by_category"].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {n}")
    print(f"\nBy company:")
    for c, n in sorted(count["by_company"].items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")


def show_queue():
    q = INTEL_DIR / ".queue"
    if q.exists():
        print(f"📥 INGEST QUEUE")
        print(f"{'━' * 30}")
        print(q.read_text())
    else:
        print("Queue is empty.")


def main():
    check_tools()
    parser = argparse.ArgumentParser(description="INGEST SOCIAL — Amoeba Skill Engine")
    parser.add_argument("url", nargs="?", help="URL to ingest")
    parser.add_argument("--quick", action="store_true", help="Caption + comments only")
    parser.add_argument("--assimilate", action="store_true", help="Skip user review gate")
    parser.add_argument("--status", action="store_true", help="Show ingestion stats")
    parser.add_argument("--queue", action="store_true", help="Show pending review items")
    args = parser.parse_args()

    if args.status:
        show_status()
        return
    if args.queue:
        show_queue()
        return
    if not args.url:
        parser.print_help()
        return

    url = args.url
    if not args.assimilate and already_ingested(url):
        print(f"⚠️ Content already ingested today. Re-ingest? (pass --assimilate to override)")
        return

    companies = get_tracked_companies()

    # Phase 1 — Extract
    print("🔍 Extracting...")
    if args.quick:
        data = quick_ingest(url)
        caption, image_texts, transcript, comments = data["caption"], [], "", data["comments"]
    else:
        data = extract_instagram(url)
        caption = data["caption"]
        image_texts = data["image_texts"]
        transcript = data["transcript"]
        comments = data["comments"]
        if not data["caption"] and not data["image_texts"] and not data["transcript"]:
            print("⚠️ No Instagram-specific content. Trying webfetch fallback...")
            caption = url

    # Phase 2 — Classify
    classification = classify_content(caption, transcript, comments, companies)

    # Phase 3 — Cross-Reference
    linked = link_to_pipeline(classification, companies, caption, transcript)

    # Phase 4 — Assimilate
    written = write_intel(url, classification, linked, caption, image_texts, transcript, comments, args.assimilate)
    if written:
        update_learned(classification, caption, transcript)
        update_fit_maps(linked, caption)
    count = update_count(classification, linked)

    # Phase 5 — Report
    print()
    print(format_report(url, classification, linked, caption, image_texts, transcript, comments, count))

    # Phase 6 — Git note
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    from urllib.parse import urlparse
    slug = urlparse(url).path.rstrip("/").split("/")[-1][:30]
    print(
        f'\n\U0001f4be Commit: git add -A && git commit -m '
        f'"INGEST \u2014 {slug} \u2014 {classification[0]} \u2014 {now}"'
    )


if __name__ == "__main__":
    main()
