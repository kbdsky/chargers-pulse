"""Categorization engine for classifying Chargers news into distinct categories."""

import re
from typing import Dict, List
from ..config import CATEGORY_RULES


class Categorizer:
    """Classifies news articles into predefined thematic categories."""

    def __init__(self, rules: Dict[str, Dict[str, any]] = None):
        self.rules = rules or CATEGORY_RULES

    def categorize_article(self, article: Dict[str, any]) -> Dict[str, any]:
        """Determine category, badge, and icon for an article."""
        title = article.get("title", "")
        summary = article.get("summary", "")
        content = f"{title} {summary}"

        # Category matching order: game, injury, roster, interview, general
        order = ["game", "injury", "roster", "interview"]

        matched_category = "general"

        for cat_key in order:
            cat_data = self.rules.get(cat_key, {})
            keywords = cat_data.get("keywords", [])
            
            matched = False
            for kw in keywords:
                # Word boundary check for short or ascii keywords
                if len(kw) <= 4 or kw.isascii():
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    if re.search(pattern, content, re.IGNORECASE):
                        matched = True
                        break
                else:
                    if kw.lower() in content.lower():
                        matched = True
                        break

            if matched:
                matched_category = cat_key
                break

        rule_info = self.rules.get(matched_category, self.rules["general"])
        article["category_key"] = matched_category
        article["category_name"] = rule_info["name"]
        article["category_badge"] = rule_info["badge"]
        article["category_icon"] = rule_info["icon"]

        return article

    def categorize_all(self, articles: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Categorize a list of articles."""
        return [self.categorize_article(art) for art in articles]
