"""Deduplication and quality filtering engine for news articles with 30-day window."""

import re
import datetime
from typing import Dict, List, Set

ERROR_PATTERNS = [
    "error 500", "server error", "that's an error", "that’s an error",
    "please try again later", "that’s all we know", "404 not found",
    "403 forbidden", "too many requests"
]


class Deduplicator:
    """Deduplicates articles based on URL and title similarity with a 30-day scope."""

    def __init__(self, similarity_threshold: float = 0.65, max_age_days: int = 31):
        self.similarity_threshold = similarity_threshold
        self.max_age_days = max_age_days

    def deduplicate(self, articles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Remove duplicate and corrupted/outdated error articles."""
        unique_articles: List[Dict[str, any]] = []
        seen_urls: Set[str] = set()
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        for art in articles:
            url = self._normalize_url(art.get("url", ""))
            title = art.get("title", "")
            summary = art.get("summary", "")
            pub_str = art.get("published", "")

            if not url or not title:
                continue

            # Filter out error pages and server failure snippets
            content_lower = f"{title} {summary}".lower()
            if any(err in content_lower for err in ERROR_PATTERNS):
                continue

            # Exclude articles older than 31 days or from past years
            if pub_str and self.max_age_days is not None:
                try:
                    pub_dt = datetime.datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                    if not pub_dt.tzinfo:
                        pub_dt = pub_dt.replace(tzinfo=datetime.timezone.utc)
                    age_days = (now_utc - pub_dt).total_seconds() / 86400
                    if age_days > self.max_age_days:
                        continue
                except Exception:
                    pass

            if url in seen_urls:
                continue

            # Check similarity with existing unique articles
            is_duplicate = False
            for existing in unique_articles:
                sim = self._calculate_title_similarity(title, existing.get("title", ""))
                if sim >= self.similarity_threshold:
                    is_duplicate = True
                    # If this one has longer summary, keep the better one
                    if len(summary) > len(existing.get("summary", "")):
                        existing["summary"] = summary
                    break

            if not is_duplicate:
                seen_urls.add(url)
                unique_articles.append(art)

        return unique_articles

    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL by stripping tracking parameters."""
        url = url.split("?utm_")[0].split("&utm_")[0]
        return url.strip().rstrip("/")

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Compute Jaccard token similarity between two titles."""
        tokens1 = self._tokenize(title1)
        tokens2 = self._tokenize(title2)

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)

        return len(intersection) / len(union)

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        """Convert string to normalized set of alphanumeric words (length >= 3)."""
        words = re.findall(r"\b\w{3,}\b", text.lower())
        stop_words = {
            "the", "and", "for", "with", "this", "that", "from", "are", "was",
            "were", "has", "have", "had", "chargers", "los", "angeles", "nfl", "news"
        }
        return {w for w in words if w not in stop_words}
