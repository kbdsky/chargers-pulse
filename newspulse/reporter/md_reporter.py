"""Markdown report generator for LA Chargers briefings."""

import os
import datetime
from typing import Dict, List


class MarkdownReporter:
    """Generates structured Markdown reports."""

    def render(
        self,
        articles: List[Dict[str, any]],
        briefing: Dict[str, any],
        title: str = "⚡ LA Chargers 종합 뉴스 인텔리전스 주간 리포트",
    ) -> str:
        """Render markdown text."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = []

        lines.append(f"# {title}")
        lines.append(f"> 📅 **생성 일시:** {now} | ⚡ **전수 수집 기사:** {len(articles)}건 | 🏈 **팀:** Los Angeles Chargers (NFL)\n")

        # 1. Executive Summary
        lines.append("## ⚡ 팀 총괄 주간 브리핑 (Executive Summary)")
        lines.append(f"### {briefing.get('headline', '')}\n")

        takeaways = briefing.get("key_takeaways", [])
        if takeaways:
            lines.append("#### 📌 핵심 주요 사항")
            for t in takeaways:
                lines.append(f"- {t}")
            lines.append("")

        trends = briefing.get("trending_keywords", [])
        if trends:
            lines.append(f"**🔥 실시간 트렌드 키워드:** {', '.join(['`#' + kw + '`' for kw in trends])}\n")

        injury = briefing.get("injury_update")
        if injury:
            lines.append(f"**📋 부상 및 53인 로스터 동향:** {injury}\n")

        outlook = briefing.get("team_outlook")
        if outlook:
            lines.append(f"**🏈 종합 코멘트:** {outlook}\n")

        # 2. Game Center
        game_center = briefing.get("game_center", {})
        if game_center and game_center.get("has_game_data"):
            lines.append("## 🏈 경기 및 매치업 분석 (Game Center)")
            lines.append(f"- **상대팀:** {game_center.get('opponent', '미정')}")
            lines.append(f"- **경기 구분:** {game_center.get('game_type', '경기')}")
            lines.append(f"- **스코어/현황:** {game_center.get('score_detected', '미확정')}")
            lines.append(f"- **⚔️ 공격진(Offense):** {game_center.get('offense_notes', '')}")
            lines.append(f"- **🛡️ 수비진(Defense):** {game_center.get('defense_notes', '')}\n")

        # 3. Top Priority Highlights
        top_highlights = briefing.get("top_highlights", [])
        if top_highlights:
            lines.append("## 🚨 최우선 핵심 뉴스 (Top Priority Highlights)\n")
            for h in top_highlights:
                url = h.get("url", "#")
                lines.append(f"### [{h.get('headline_kr', h.get('title'))}]({url})")
                lines.append(f"*중요도: {h.get('importance_score', 0)}점 ({h.get('priority_tier', '')}) | 출처: {h.get('source', '')}*")
                for b in h.get("summary_bullets_kr", []):
                    lines.append(f"- {b}")
                lines.append("")

        lines.append("---\n")

        # 4. Group by Category
        categories = {
            "game": "⚡ 경기 결과 및 프리뷰 소식",
            "injury": "📋 부상 및 로스터 변동 리포트",
            "roster": "🎯 선수 계약 및 영입/트레이드",
            "interview": "🎙️ 감독 및 선수 주요 인터뷰",
            "general": "⚡ 팀 일반 소식",
        }

        articles_by_cat: Dict[str, List[Dict[str, any]]] = {k: [] for k in categories}
        for art in articles:
            cat_k = art.get("category_key", "general")
            if cat_k in articles_by_cat:
                articles_by_cat[cat_k].append(art)
            else:
                articles_by_cat["general"].append(art)

        lines.append("## 📰 전체 수집 뉴스 카테고리별 아카이브\n")

        for cat_key, cat_title in categories.items():
            cat_articles = articles_by_cat[cat_key]
            if not cat_articles:
                continue

            lines.append(f"### {cat_title} ({len(cat_articles)}건)\n")

            for art in cat_articles:
                date_str = art.get("published", "")[:10]
                source = art.get("source", "Unknown")
                headline_kr = art.get("headline_kr", art.get("title", ""))
                orig_title = art.get("title", "")
                url = art.get("url", "#")
                score = art.get("importance_score", 0)

                lines.append(f"#### [{headline_kr}]({url}) `[점수:{score}]`")
                lines.append(f"*출처: {source} | 일자: {date_str}*")
                lines.append(f"- **원제:** {orig_title}")

                bullets = art.get("summary_bullets_kr", [])
                for b in bullets:
                    lines.append(f"- {b}")
                lines.append("")

        lines.append("---\n")
        lines.append("*⚡ Generated automatically by NewsPulse 2.0 (LA Chargers Intelligence)*\n")

        return "\n".join(lines)

    def save(
        self,
        output_path: str,
        articles: List[Dict[str, any]],
        briefing: Dict[str, any],
        title: str = "⚡ LA Chargers 종합 뉴스 인텔리전스 주간 리포트",
    ) -> str:
        """Render and write markdown report to file."""
        md_content = self.render(articles=articles, briefing=briefing, title=title)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        return output_path
