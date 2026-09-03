"""Deduplication and quality filtering engine for news articles."""

import re
from typing import Dict, List, Set

ERROR_PATTERNS = [
    "error 500", "server error", "that's an error", "that’s an error",
    "please try again later", "that’s all we know", "404 not found",
    "403 forbidden", "too many requests"
]


class Deduplicator:
    """Deduplicates articles based on URL and title similarity, and filters out error items."""

    def __init__(self, similarity_threshold: float = 0.65):
        self.similarity_threshold = similarity_threshold

    def deduplicate(self, articles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Remove duplicate and corrupted error articles."""
        unique_articles: List[Dict[str, any]] = []
        seen_urls: Set[str] = set()

        for art in articles:
            url = self._normalize_url(art.get("url", ""))
            title = art.get("title", "")
            summary = art.get("summary", "")

            if not url or not title:
                continue

            # Filter out error pages and server failure snippets
            content_lower = f"{title} {summary}".lower()
            if any(err in content_lower for err in ERROR_PATTERNS):
                continue

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
