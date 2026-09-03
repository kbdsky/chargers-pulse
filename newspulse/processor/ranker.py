"""Importance Scoring and Smart Article Ranker for Chargers News."""

import re
import datetime
from typing import Dict, List, Tuple


class ArticleRanker:
    """Calculates importance score (0-100) and curates top priority highlights."""

    # High-impact football/team impact keywords
    HIGH_IMPACT_KEYWORDS = {
        "injury": 25,
        "injured": 20,
        "surgery": 25,
        "ir": 20,
        "out": 15,
        "concussion": 25,
        "ankle": 15,
        "starter": 20,
        "53-man": 25,
        "roster": 15,
        "trade": 25,
        "sign": 15,
        "contract": 20,
        "recap": 20,
        "score": 15,
        "highlights": 15,
        "touchdown": 15,
        "win": 15,
        "loss": 15,
        "harbaugh": 15,
        "herbert": 20,
        "alt": 15,
        "bosa": 15,
        "mack": 15,
    }

    def score_article(self, article: Dict[str, any], all_articles: List[Dict[str, any]] = None) -> int:
        """Calculate an importance score from 0 to 100 for an article."""
        score = 30  # Baseline

        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()
        content = f"{title} {summary}"

        # 1. Keyword Impact (Max +40)
        keyword_score = 0
        for kw, pts in self.HIGH_IMPACT_KEYWORDS.items():
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, content, re.IGNORECASE):
                keyword_score += pts
                if keyword_score >= 40:
                    break
        score += min(keyword_score, 40)

        # 2. Source Credibility (Max +15)
        source = article.get("source", "").lower()
        if "bolts from the blue" in source or "espn" in source:
            score += 15
        elif "yardbarker" in source:
            score += 10
        elif "google news" in source:
            score += 8

        # 3. Cross-Coverage / Repetition across outlets (Max +20)
        if all_articles:
            cross_coverage = 0
            title_words = set(re.findall(r"\b\w{4,}\b", title)) - {"chargers", "angeles", "with", "from", "that"}
            for other in all_articles:
                if other is not article:
                    other_title = other.get("title", "").lower()
                    overlap = sum(1 for w in title_words if w in other_title)
                    if overlap >= 2:
                        cross_coverage += 5
            score += min(cross_coverage, 20)

        # 4. Content Richness (Max +10)
        if len(summary) > 100:
            score += 10
        elif len(summary) > 40:
            score += 5

        # 5. Freshness Bonus (Max +10)
        pub_str = article.get("published", "")
        if pub_str:
            try:
                # Basic check for recent ISO date
                pub_date = datetime.datetime.fromisoformat(pub_str[:19])
                now = datetime.datetime.now()
                days_diff = (now - pub_date).total_seconds() / 86400.0
                if days_diff <= 1.0:
                    score += 10
                elif days_diff <= 3.0:
                    score += 5
            except Exception:
                pass

        final_score = min(max(score, 10), 100)
        article["importance_score"] = final_score

        # Assign Priority Tier
        if final_score >= 75:
            article["priority_tier"] = "🚨 긴급/핵심"
            article["priority_class"] = "tier-critical"
        elif final_score >= 55:
            article["priority_tier"] = "⚡ 주요"
            article["priority_class"] = "tier-high"
        else:
            article["priority_tier"] = "📰 일반"
            article["priority_class"] = "tier-normal"

        return final_score

    def rank_articles(self, articles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Score and sort all articles by importance."""
        for art in articles:
            self.score_article(art, all_articles=articles)

        # Sort descending by importance_score
        return sorted(articles, key=lambda x: x.get("importance_score", 0), reverse=True)

    def get_top_priority(self, articles: List[Dict[str, any]], limit: int = 5) -> List[Dict[str, any]]:
        """Extract the top critical articles."""
        ranked = self.rank_articles(articles)
        return ranked[:limit]
