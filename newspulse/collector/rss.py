"""RSS & Atom feed collector for Chargers news with freshness filtering."""

import logging
import datetime
from typing import Dict, List, Optional
import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class RSSCollector:
    """Collects news articles from RSS & Atom feeds with recency filtering."""

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 15):
        self.headers = headers or {"User-Agent": USER_AGENT}
        self.timeout = timeout

    def fetch_feed(
        self,
        feed_url: str,
        source_name: str = "",
        filter_chargers: bool = False,
        limit: int = 100,
        max_age_days: Optional[int] = 10,
    ) -> List[Dict[str, any]]:
        """Fetch and parse an RSS feed URL with recency filter."""
        articles = []
        now_utc = datetime.datetime.now(datetime.timezone.utc)

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

                # Filter out ancient/outdated articles
                if pub_date and max_age_days is not None:
                    try:
                        pub_utc = pub_date if pub_date.tzinfo else pub_date.replace(tzinfo=datetime.timezone.utc)
                        age_days = (now_utc - pub_utc).total_seconds() / 86400
                        if age_days > max_age_days:
                            continue
                    except Exception:
                        pass

                if filter_chargers:
                    combined_text = f"{title} {summary_text}".lower()
                    charger_kw = ["charger", "chargers", "herbert", "harbaugh", "bosa", "derwin", "alt", "ladd", "dobbins"]
                    if not any(k in combined_text for k in charger_kw):
                        continue

                article = {
                    "title": title,
                    "url": link,
                    "summary": summary_text,
                    "published": pub_date.isoformat() if pub_date else now_utc.isoformat(),
                    "source": feed_title,
                    "author": author,
                    "raw_entry": entry,
                }
                articles.append(article)

        except Exception as e:
            logger.warning(f"Failed to fetch feed {feed_url}: {e}")

        return articles

    def fetch_multiple_feeds(
        self,
        feed_configs: List[Dict[str, any]],
        limit_per_feed: int = 50,
        max_age_days: int = 10,
    ) -> List[Dict[str, any]]:
        """Fetch articles across a list of configured feeds."""
        all_articles = []
        for conf in feed_configs:
            url = conf.get("url")
            name = conf.get("name", "")
            filter_flag = conf.get("filter_chargers", False)
            results = self.fetch_feed(
                feed_url=url,
                source_name=name,
                filter_chargers=filter_flag,
                limit=limit_per_feed,
                max_age_days=max_age_days,
            )
            all_articles.extend(results)
        return all_articles

    @staticmethod
    def _clean_html(raw_html: str) -> str:
        """Strip HTML tags and normalize whitespace."""
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=" ")
        return " ".join(text.split())

    @staticmethod
    def _parse_date(entry: dict) -> Optional[datetime.datetime]:
        """Extract and normalize publication datetime."""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                import time
                return datetime.datetime.fromtimestamp(
                    time.mktime(entry.published_parsed), tz=datetime.timezone.utc
                )
            except Exception:
                pass
        if hasattr(entry, "updated_parsed") and entry.updated_parsed:
            try:
                import time
                return datetime.datetime.fromtimestamp(
                    time.mktime(entry.updated_parsed), tz=datetime.timezone.utc
                )
            except Exception:
                pass
        return None
