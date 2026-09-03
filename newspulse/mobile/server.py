"""FastAPI Mobile Backend Server for ChargersPulse PWA and Android App."""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from ..config import CHARGERS_RSS_FEEDS
from ..collector import RSSCollector, GoogleNewsCollector
from ..processor import (
    Deduplicator,
    Categorizer,
    Summarizer,
    ArticleRanker,
    DynamicKeywordTracker,
    GameAnalyzer,
)
from ..reporter import HTMLReporter, MarkdownReporter

logger = logging.getLogger("newspulse.mobile")

app = FastAPI(title="ChargersPulse Mobile API", version="2.0.0")

# Enable CORS for cross-device mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
REPORTS_DIR = Path(os.getcwd()) / "reports"
CACHE_JSON_PATH = REPORTS_DIR / "latest_mobile_data.json"

# In-memory cached data
_cached_payload: Dict[str, any] = {}


def load_cached_data() -> Dict[str, any]:
    """Load cached briefing data if available."""
    global _cached_payload
    if _cached_payload:
        return _cached_payload

    if CACHE_JSON_PATH.exists():
        try:
            with open(CACHE_JSON_PATH, "r", encoding="utf-8") as f:
                _cached_payload = json.load(f)
                return _cached_payload
        except Exception as e:
            logger.warning(f"Error reading cache: {e}")

    # If no cache exists, run an initial quick collection
    return run_full_pipeline()


def run_full_pipeline() -> Dict[str, any]:
    """Execute full unconstrained news pipeline and update cache."""
    global _cached_payload
    logger.info("⚡ Executing news pipeline for mobile...")

    # 1. Collect
    rss = RSSCollector()
    rss_arts = rss.fetch_multiple_feeds(CHARGERS_RSS_FEEDS, limit_per_feed=40)

    kw_tracker = DynamicKeywordTracker()
    queries = kw_tracker.get_search_queries()
    gnews = GoogleNewsCollector()
    gnews_arts = gnews.search_queries(queries, limit_per_query=20)

    raw_articles = rss_arts + gnews_arts

    # 2. Deduplicate
    dedup = Deduplicator(similarity_threshold=0.6)
    unique_articles = dedup.deduplicate(raw_articles)

    # 3. Dynamic keywords
    trend_state = kw_tracker.extract_trends_from_articles(unique_articles)

    # 4. Categorize, Rank, Summarize
    cat = Categorizer()
    categorized = cat.categorize_all(unique_articles)

    ranker = ArticleRanker()
    ranked = ranker.rank_articles(categorized)

    summarizer = Summarizer()
    summarized = summarizer.summarize_all(ranked)
    briefing = summarizer.generate_executive_briefing(summarized)

    # 5. Save HTML and Markdown reports as well
    os.makedirs(REPORTS_DIR, exist_ok=True)
    html_rep = HTMLReporter()
    html_rep.save(str(REPORTS_DIR / "chargers_briefing_latest.html"), summarized, briefing)
    md_rep = MarkdownReporter()
    md_rep.save(str(REPORTS_DIR / "chargers_briefing_latest.md"), summarized, briefing)

    payload = {
        "status": "success",
        "briefing": briefing,
        "articles": summarized,
        "total_count": len(summarized),
    }

    # Save cache
    with open(CACHE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    _cached_payload = payload
    return payload


# API Endpoints
@app.get("/api/briefing")
def get_briefing():
    """Return latest executive briefing and articles."""
    return load_cached_data()


@app.post("/api/refresh")
def refresh_data():
    """Trigger full news collection and return fresh data."""
    return run_full_pipeline()


@app.get("/api/articles")
def get_articles(category: Optional[str] = None, q: Optional[str] = None):
    """Filter articles by category or keyword."""
    data = load_cached_data()
    articles = data.get("articles", [])

    if category:
        articles = [a for a in articles if a.get("category_key") == category]

    if q:
        q_lower = q.lower()
        articles = [
            a for a in articles
            if q_lower in a.get("title", "").lower()
            or q_lower in a.get("headline_kr", "").lower()
            or q_lower in " ".join(a.get("summary_bullets_kr", [])).lower()
        ]

    return {"status": "success", "articles": articles, "count": len(articles)}


# Static files & PWA routes
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/manifest.json")
def get_manifest():
    return FileResponse(STATIC_DIR / "manifest.json", media_type="application/json")


@app.get("/service-worker.js")
def get_service_worker():
    return FileResponse(STATIC_DIR / "service-worker.js", media_type="application/javascript")


@app.get("/")
def get_root():
    return FileResponse(STATIC_DIR / "index.html")
