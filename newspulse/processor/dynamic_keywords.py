"""Dynamic Keyword Discovery & Trend Tracking Engine."""

import os
import json
import re
from collections import Counter
from typing import Dict, List, Set, Tuple
from ..config import DYNAMIC_KEYWORD_FILE, NFL_TEAMS, BASE_GOOGLE_NEWS_QUERIES

STOP_WORDS = {
    "the", "and", "for", "with", "this", "that", "from", "are", "was", "were",
    "has", "have", "had", "chargers", "angeles", "los", "nfl", "football",
    "news", "team", "said", "will", "been", "they", "their", "after", "into",
    "about", "over", "more", "also", "what", "which", "when", "where", "who",
    "how", "all", "out", "new", "get", "got", "can", "could", "would", "should",
    "take", "takes", "took", "back", "first", "game", "week", "season", "time"
}


class DynamicKeywordTracker:
    """Discovers trending topics, players, and auto-updates search keywords."""

    def __init__(self, cache_file: str = DYNAMIC_KEYWORD_FILE):
        self.cache_file = cache_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, any]:
        """Load persistent keyword trends from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "trending_keywords": [],
            "emerging_players": [],
            "opponents": [],
            "expanded_queries": list(BASE_GOOGLE_NEWS_QUERIES),
            "last_updated": None,
        }

    def _save_state(self):
        """Save keyword trends to file."""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def extract_trends_from_articles(self, articles: List[Dict[str, any]]) -> Dict[str, any]:
        """Analyze full article collection and extract live trending keywords and entities."""
        if not articles:
            return self.state

        word_counter = Counter()
        bigram_counter = Counter()
        detected_opponents = Counter()
        detected_entities = Counter()

        for art in articles:
            title = art.get("title", "")
            summary = art.get("summary", "")
            text = f"{title} {summary}"

            # 1. Opponent Team detection
            lower_text = text.lower()
            for opp_key, opp_name in NFL_TEAMS.items():
                if re.search(r"\b" + re.escape(opp_key) + r"\b", lower_text):
                    detected_opponents[opp_name] += 1

            # 2. Capitalized entity phrase extraction (e.g., "Joe Alt", "Deane Leonard", "Preseason Week")
            entities = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text)
            for ent in entities:
                ent_clean = ent.strip()
                if not any(sw in ent_clean.lower() for sw in ["Los Angeles", "San Francisco", "United States", "Good Morning", "New York"]):
                    detected_entities[ent_clean] += 1

            # 3. Clean word tokens (length >= 4)
            words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{4,}\b", text) if w.lower() not in STOP_WORDS]
            word_counter.update(words)

            # 4. Bigrams (e.g. "joint practice", "practice squad", "offensive line")
            for i in range(len(words) - 1):
                bg = f"{words[i]} {words[i+1]}"
                bigram_counter[bg] += 1

        top_words = [w for w, _ in word_counter.most_common(12)]
        top_bigrams = [bg for bg, _ in bigram_counter.most_common(8)]
        top_entities = [ent for ent, _ in detected_entities.most_common(8)]
        top_opponents = [opp for opp, _ in detected_opponents.most_common(4)]

        # Combine into trending keywords
        trending = list(dict.fromkeys(top_bigrams[:5] + top_entities[:5] + top_words[:6]))

        # Dynamically build new Google News queries based on current trends
        expanded = list(BASE_GOOGLE_NEWS_QUERIES)
        for ent in top_entities[:3]:
            q = f"Chargers {ent}"
            if q not in expanded:
                expanded.append(q)

        for opp in top_opponents[:2]:
            opp_short = opp.split("(")[-1].replace(")", "").strip()
            q = f"Chargers vs {opp_short}"
            if q not in expanded:
                expanded.append(q)

        import datetime
        self.state = {
            "trending_keywords": trending,
            "emerging_players": top_entities[:6],
            "opponents": top_opponents,
            "expanded_queries": expanded[:10],
            "last_updated": datetime.datetime.now().isoformat(),
        }
        self._save_state()
        return self.state

    def get_search_queries(self) -> List[str]:
        """Get the current dynamic search queries for collectors."""
        return self.state.get("expanded_queries", BASE_GOOGLE_NEWS_QUERIES)
