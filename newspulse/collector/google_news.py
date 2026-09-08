"""Google News RSS collector for targeted and dynamic keyword searches with freshness constraints."""

import urllib.parse
from typing import Dict, List, Optional
from .rss import RSSCollector


class GoogleNewsCollector:
    """Fetches real-time news via Google News RSS search endpoints (restricted to recent news)."""

    def __init__(self, hl: str = "en-US", gl: str = "US", ceid: str = "US:en"):
        self.hl = hl
        self.gl = gl
        self.ceid = ceid
        self.rss_collector = RSSCollector()

    def build_url(self, query: str, when: str = "7d") -> str:
        """Construct a Google News RSS search URL with freshness constraint (when:7d)."""
        q_clean = query.strip()
        if "when:" not in q_clean and when:
            q_clean = f"{q_clean} when:{when}"

        encoded_query = urllib.parse.quote(q_clean)
        return (
            f"https://news.google.com/rss/search?q={encoded_query}"
            f"&hl={self.hl}&gl={self.gl}&ceid={self.ceid}"
        )

    def search(self, query: str, limit: int = 50, when: str = "7d") -> List[Dict[str, any]]:
        """Search Google News for articles matching the query within recent time window."""
        url = self.build_url(query, when=when)
        articles = self.rss_collector.fetch_feed(
            feed_url=url,
            source_name="Google News",
            limit=limit,
            max_age_days=10,
        )

        for art in articles:
            title = art.get("title", "")
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                art["title"] = parts[0].strip()
                art["source"] = parts[1].strip()
            art["search_query"] = query

        return articles

    def search_queries(self, queries: List[str], limit_per_query: int = 25, when: str = "7d") -> List[Dict[str, any]]:
        """Search across multiple query keywords within recent time window."""
        all_articles = []
        for q in queries:
            results = self.search(q, limit=limit_per_query, when=when)
            all_articles.extend(results)
        return all_articles
