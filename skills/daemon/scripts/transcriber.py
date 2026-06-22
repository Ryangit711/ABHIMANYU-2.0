"""
Video/Reel Transcriber — DAEMON Enhancement
ABHIMANYU 2.0

Downloads audio from Instagram reels, X.com videos, YouTube, etc.
Transcribes using available backends:
  - Google Web Speech (free, no key) — works for short clips
  - OpenAI Whisper API (requires key) — best quality
  - Placeholder for local whisper model

Built on top of existing system. Never modifies existing files.
"""

import json, os, re, subprocess, sys, time, tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
DAEMON_DIR = os.path.join(DATA_DIR, "daemon")
TRANSCRIPT_CACHE_DIR = os.path.join(DAEMON_DIR, "transcripts")
SOCIAL_CACHE_DIR = os.path.join(DAEMON_DIR, "social_cache")
TEMP_DIR = os.path.join(DAEMON_DIR, "temp_audio")

def ensure_dirs():
    for d in [DAEMON_DIR, TRANSCRIPT_CACHE_DIR, SOCIAL_CACHE_DIR, TEMP_DIR]:
        os.makedirs(d, exist_ok=True)


def get_cache_key(url: str) -> str:
    clean = re.sub(r'[^a-zA-Z0-9]', '_', url.split("?")[0].split("&")[0])[:80]
    return clean


def is_cached(url: str) -> dict | None:
    key = get_cache_key(url)
    cache_file = os.path.join(TRANSCRIPT_CACHE_DIR, f"{key}.json")
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            cached = json.load(f)
            if time.time() - cached.get("cached_at", 0) < 86400:
                return cached
    return None


def save_cache(url: str, data: dict):
    key = get_cache_key(url)
    cache_file = os.path.join(TRANSCRIPT_CACHE_DIR, f"{key}.json")
    data["cached_at"] = time.time()
    data["cache_key"] = key
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)


def download_audio(url: str) -> tuple:
    """Download audio from a video URL using yt-dlp. Returns (path, title)."""
    ensure_dirs()
    if not HAS_YTDLP:
        return None, "yt-dlp not installed"

    try:
        ts = int(time.time())
        output_template = os.path.join(TEMP_DIR, f"audio_{ts}.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }],
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "unknown")
            expected = os.path.join(TEMP_DIR, f"audio_{ts}.wav")
            if os.path.exists(expected):
                return expected, title
            for f in os.listdir(TEMP_DIR):
                if f.startswith(f"audio_{ts}"):
                    return os.path.join(TEMP_DIR, f), title
            return None, title

    except Exception as e:
        return None, str(e)


def get_audio_duration(audio_path: str) -> float:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True, timeout=10
        )
        return float(r.stdout.strip())
    except:
        return 0


def split_audio(audio_path: str, chunk_seconds: int = 60) -> list[str]:
    """Split audio into chunks of chunk_seconds. Returns list of chunk paths."""
    duration = get_audio_duration(audio_path)
    if duration <= chunk_seconds:
        return [audio_path]

    chunks = []
    base = os.path.splitext(audio_path)[0]
    for start in range(0, int(duration), chunk_seconds):
        chunk_file = f"{base}_chunk_{start}.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path, "-ss", str(start),
             "-t", str(chunk_seconds), "-acodec", "pcm_s16le",
             "-ar", "16000", "-ac", "1", chunk_file],
            capture_output=True, timeout=30
        )
        if os.path.exists(chunk_file):
            chunks.append(chunk_file)
    return chunks


def transcribe_google(audio_path: str, language: str = "en-US") -> str:
    """Transcribe using Google Web Speech API (free, no key needed).
    Automatically splits long audio into 60s chunks."""
    if not HAS_SR:
        return None

    chunks = split_audio(audio_path, 60)
    full_text = []
    recognizer = sr.Recognizer()

    for chunk_path in chunks:
        try:
            with sr.AudioFile(chunk_path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language)
            full_text.append(text)
        except sr.UnknownValueError:
            full_text.append("[unintelligible]")
        except sr.RequestError as e:
            full_text.append(f"[error: {e}]")
        except Exception:
            full_text.append("[error]")
        finally:
            if chunk_path != audio_path and os.path.exists(chunk_path):
                try:
                    os.remove(chunk_path)
                except:
                    pass

    return " ".join(full_text).strip() or None


def transcribe_whisper_api(audio_path: str, api_key: str = None) -> str:
    """
    Transcribe using OpenAI Whisper API.
    Requires OPENAI_API_KEY environment variable or passed directly.
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
            )
        return transcript.text
    except Exception as e:
        return f"[Whisper API error: {e}]"


def transcribe(url: str, force: bool = False) -> dict:
    """
    Main entry point. Downloads audio from URL and transcribes it.
    Returns dict with transcription and metadata.
    """
    ensure_dirs()

    if not force:
        cached = is_cached(url)
        if cached:
            return cached

    result = {
        "url": url,
        "title": None,
        "platform": None,
        "transcription": None,
        "transcription_method": None,
        "duration_seconds": None,
        "error": None,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    # Detect platform
    if "instagram.com" in url:
        result["platform"] = "instagram"
    elif "x.com" in url or "twitter.com" in url:
        result["platform"] = "x.com"
    elif "youtube.com" in url or "youtu.be" in url:
        result["platform"] = "youtube"
    elif "tiktok.com" in url:
        result["platform"] = "tiktok"
    else:
        result["platform"] = "unknown"

    # Download audio
    audio_path, audio_title = download_audio(url)
    result["title"] = audio_title

    if not audio_path or not os.path.exists(audio_path):
        err_detail = audio_title if audio_title and "Error" in str(audio_title) else "yt-dlp may need cookies for this platform"
        result["error"] = f"Could not download audio: {err_detail}"
        save_cache(url, result)
        return result

    try:
        # Get duration
        result["duration_seconds"] = get_audio_duration(audio_path)

        # Try Google Speech first (free, auto-chunks long audio)
        text = transcribe_google(audio_path)
        if text and not text.startswith("[error"):
            result["transcription"] = text
            result["transcription_method"] = "google_web_speech"
        else:
            # Try Whisper API if key available
            text = transcribe_whisper_api(audio_path)
            if text:
                result["transcription"] = text
                result["transcription_method"] = "whisper_api"

    except Exception as e:
        result["error"] = str(e)
    finally:
        # Cleanup temp files
        try:
            os.remove(audio_path)
        except:
            pass

    if not result.get("transcription"):
        result["error"] = result.get("error") or "No transcription method succeeded. Try: whisper_api (set OPENAI_API_KEY) or whisper.cpp (install locally)."

    save_cache(url, result)
    return result


def transcribe_and_analyze(url: str) -> dict:
    """
    Transcribe a video URL, then run the transcribed text through
    the social intelligence cross-reference engine.
    """
    # Get transcription
    transcript_result = transcribe(url)

    # If we got text, run it through cross-reference
    if transcript_result.get("transcription"):
        # Import the cross-reference function from social_intelligence_layer
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        try:
            from social_intelligence_layer import ingest_social_post, is_already_known, load_existing_knowledge
            knowledge = load_existing_knowledge()
            analysis = is_already_known(transcript_result["transcription"], knowledge)
            transcript_result["cross_reference"] = analysis
        except ImportError:
            transcript_result["cross_reference"] = {"error": "Cross-reference engine not available"}
    else:
        transcript_result["cross_reference"] = {"error": "No transcription to analyze"}

    return transcript_result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <url> [--analyze]")
        print("  <url>       Instagram reel, X.com video, YouTube, or TikTok URL")
        print("  --analyze   Also run cross-reference against system knowledge")
        sys.exit(1)

    url = sys.argv[1]
    do_analyze = "--analyze" in sys.argv

    if do_analyze:
        result = transcribe_and_analyze(url)
    else:
        result = transcribe(url)

    print(json.dumps(result, indent=2, default=str))
