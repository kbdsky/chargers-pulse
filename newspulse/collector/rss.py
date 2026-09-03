"""RSS & Atom feed collector for Chargers news."""

import logging
import datetime
from typing import Dict, List, Optional
import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class RSSCollector:
    """Collects news articles from RSS & Atom feeds without arbitrary limits."""

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 15):
        self.headers = headers or {"User-Agent": USER_AGENT}
        self.timeout = timeout

    def fetch_feed(
        self,
        feed_url: str,
        source_name: str = "",
        filter_chargers: bool = False,
        limit: int = 100,
    ) -> List[Dict[str, any]]:
        """Fetch and parse an RSS feed URL."""
        articles = []
        try:
            response = requests.get(feed_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            parsed = feedparser.parse(response.content)

            feed_title = source_name or parsed.feed.get("title", "RSS Feed")

            for entry in parsed.entries[:limit]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                raw_summary = entry.get("summary") or entry.get("description", "")
                summary_text = self._clean_html(raw_summary)
                author = entry.get("author") or entry.get("dc_creator", "")
                pub_date = self._parse_date(entry)

                if filter_chargers:
                    combined_text = f"{title} {summary_text}".lower()
                    charger_kw = ["charger", "chargers", "herbert", "harbaugh", "bosa", "derwin", "alt", "ladd", "dobbins"]
                    if not any(k in combined_text for k in charger_kw):
                        continue

                article = {
                    "title": title,
                    "url": link,
                    "summary": summary_text,
                    "published": pub_date.isoformat() if pub_date else datetime.datetime.now().isoformat(),
                    "source": feed_title,
                    "author": author,
                    "raw_entry": entry,
                }
                articles.append(article)

        except Exception as e:
            logger.warning(f"Failed to fetch feed {feed_url}: {e}")

        return articles

    def fetch_multiple_feeds(self, feeds_config: List[Dict[str, any]], limit_per_feed: int = 50) -> List[Dict[str, any]]:
        """Fetch articles across a list of configured feeds."""
        all_articles = []
        for cfg in feeds_config:
            feed_url = cfg.get("url")
            name = cfg.get("name", "")
            filter_chargers = cfg.get("filter_chargers", False)
            if feed_url:
                items = self.fetch_feed(
                    feed_url=feed_url,
                    source_name=name,
                    filter_chargers=filter_chargers,
                    limit=limit_per_feed,
                )
                all_articles.extend(items)
        return all_articles

    @staticmethod
    def _clean_html(raw_html: str) -> str:
        """Strip HTML tags and normalize whitespace."""
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        return " ".join(soup.get_text().split())

    @staticmethod
    def _parse_date(entry: dict) -> Optional[datetime.datetime]:
        """Attempt to parse date from entry tuple or string."""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                return datetime.datetime(*entry.published_parsed[:6])
            except Exception:
                pass
        if hasattr(entry, "updated_parsed") and entry.updated_parsed:
            try:
                return datetime.datetime(*entry.updated_parsed[:6])
            except Exception:
                pass
        return None
