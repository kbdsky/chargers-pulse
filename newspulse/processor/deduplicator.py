"""Deduplication and smart story clustering engine for news articles."""

import re
import datetime
from typing import Dict, List, Set, Optional

ERROR_PATTERNS = [
    "error 500", "server error", "that's an error", "that’s an error",
    "please try again later", "that’s all we know", "404 not found",
    "403 forbidden", "too many requests"
]


class Deduplicator:
    """Smart story clustering and deduplication engine that merges redundant news coverage."""

    def __init__(self, similarity_threshold: float = 0.40, max_age_days: int = 31):
        self.similarity_threshold = similarity_threshold
        self.max_age_days = max_age_days

    def deduplicate(self, articles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Remove redundant duplicate articles and cluster similar media coverage."""
        unique_articles: List[Dict[str, any]] = []
        seen_urls: Set[str] = set()
        seen_topics: Dict[str, Dict[str, any]] = {}
        now_utc = datetime.datetime.now(datetime.timezone.utc)

        # Sort input by length of summary (longer/richer articles processed first)
        sorted_articles = sorted(articles, key=lambda a: len(a.get("summary", "")), reverse=True)

        for art in sorted_articles:
            url = self._normalize_url(art.get("url", ""))
            title = art.get("title", "").strip()
            summary = art.get("summary", "").strip()
            pub_str = art.get("published", "")
            source = art.get("source", "").strip()

            if not url or not title:
                continue

            # 1. Filter out error pages and server failure snippets
            content_lower = f"{title} {summary}".lower()
            if any(err in content_lower for err in ERROR_PATTERNS):
                continue

            # 2. Exclude articles older than 31 days or from past years
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

            # 3. Topic Signature Key (Entity + Key Action)
            topic_key = self._extract_topic_signature(title)

            # Check for existing story cluster
            is_duplicate = False
            for existing in unique_articles:
                sim = self._calculate_title_similarity(title, existing.get("title", ""))
                existing_topic = self._extract_topic_signature(existing.get("title", ""))

                # Match by high text similarity OR identical topic signature
                if sim >= self.similarity_threshold or (topic_key and topic_key == existing_topic):
                    is_duplicate = True
                    # Add to related sources
                    rel_sources = existing.setdefault("related_sources", [existing.get("source", "")])
                    if source and source not in rel_sources:
                        rel_sources.append(source)
                    # Keep the richer summary
                    if len(summary) > len(existing.get("summary", "")):
                        existing["summary"] = summary
                        existing["title"] = title
                        existing["url"] = url
                    break

            if not is_duplicate:
                art["related_sources"] = [source] if source else []
                seen_urls.add(url)
                unique_articles.append(art)

        return unique_articles

    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL by stripping tracking parameters."""
        url = url.split("?utm_")[0].split("&utm_")[0]
        return url.strip().rstrip("/")

    def _extract_topic_signature(self, title: str) -> Optional[str]:
        """Extract a simplified canonical topic signature from headline."""
        t_low = title.lower()

        # 1. Player Injury & Practice Status Coverage
        key_players = [
            "mcconkey", "herbert", "bosa", "alt", "chark", "slater",
            "pipkins", "molden", "dupree", "dobbins", "edwards",
            "mack", "derwin", "johnston", "palmer", "hart", "tart"
        ]
        for player in key_players:
            if player in t_low:
                if any(w in t_low for w in ["injury", "injured", "practice", "miss", "out", "questionable", "dnp", "rib", "ankle", "knee", "hand", "wrist", "hip", "ir", "status"]):
                    week_prefix = "w2" if ("raiders" in t_low or "week 2" in t_low or "week-2" in t_low) else "w1"
                    return f"topic:injury:{week_prefix}:{player}"

        # 2. Key recurring team events
        if "53-man" in t_low or "roster cut" in t_low or "initial 53" in t_low or "reduce roster" in t_low or "roster trim" in t_low:
            return "topic:53_man_roster"
        if "captain" in t_low:
            return "topic:captains_named"
        if "depth chart" in t_low:
            return "topic:depth_chart"
        if "injury report" in t_low:
            for w in range(1, 19):
                if f"week {w}" in t_low or f"week{w}" in t_low:
                    return f"topic:injury_report:w{w}"
            if "raiders" in t_low:
                return "topic:injury_report:w2"
            return "topic:injury_report:w1"

        # 3. Game Recaps & Matchup Previews
        for opp in ["cardinals", "raiders", "chiefs", "broncos", "49ers", "rams", "texans", "cowboys", "giants", "eagles"]:
            if opp in t_low and any(w in t_low for w in ["recap", "highlight", "win", "loss", "defeat", "score", "preview"]):
                return f"topic:game:{opp}"

        return None

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
            "were", "has", "have", "had", "chargers", "los", "angeles", "nfl", "news",
            "what", "when", "where", "how", "why", "after", "into", "over", "before"
        }
        return {w for w in words if w not in stop_words}
