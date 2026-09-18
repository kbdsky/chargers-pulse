"""Summarization engine supporting high-quality Korean sports NLP synthesis and Injury Table integration.
Strictly preserves player names, team names, and proper nouns in English while formatting fluent Korean summaries.
"""

import os
import re
import logging
from typing import Dict, List, Optional
from .game_analyzer import GameAnalyzer
from .dynamic_keywords import DynamicKeywordTracker
from .ranker import ArticleRanker
from .translator import KoreanTranslator
from .schedule_manager import ScheduleManager
from .injury_tracker import InjuryTracker

logger = logging.getLogger(__name__)

KEY_PLAYERS_EN = {
    "herbert": "Justin Herbert (QB)",
    "harbaugh": "Jim Harbaugh (HC)",
    "alt": "Joe Alt (OT)",
    "mcconkey": "Ladd McConkey (WR)",
    "johnston": "Quentin Johnston (WR)",
    "palmer": "Joshua Palmer (WR)",
    "chark": "DJ Chark Jr. (WR)",
    "bosa": "Joey Bosa (OLB)",
    "mack": "Khalil Mack (OLB)",
    "derwin": "Derwin James Jr. (S)",
    "dobbins": "J.K. Dobbins (RB)",
    "edwards": "Gus Edwards (RB)",
    "hampton": "Omarion Hampton (RB)",
    "slater": "Rashawn Slater (OT)",
    "biadasz": "Tyler Biadasz (C)",
    "minter": "Jesse Minter (DC)",
    "roman": "Greg Roman (OC)",
    "hortiz": "Joe Hortiz (GM)",
}


class Summarizer:
    """Produces fluent Korean summaries and structured intelligence briefings."""

    def __init__(self, gemini_api_key: Optional[str] = None):
        self.gemini_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.game_analyzer = GameAnalyzer()
        self.keyword_tracker = DynamicKeywordTracker()
        self.ranker = ArticleRanker()
        self.translator = KoreanTranslator()
        self.schedule_manager = ScheduleManager()
        self.injury_tracker = InjuryTracker()

    def summarize_article(self, article: Dict[str, any]) -> Dict[str, any]:
        """Generate high-quality Korean headline and contextual summary bullets with English proper nouns."""
        title = article.get("title", "")
        summary = article.get("summary", "")
        category_name = article.get("category_name", "팀 소식")

        # 1. Headline: Korean translation with English proper nouns
        kr_headline = self.translator.translate_text(title, max_chars=180)
        if not self.translator._is_valid_translation(kr_headline):
            kr_headline = self.translator.synthesize_korean_sentence(title)
        article["headline_kr"] = kr_headline if kr_headline else title

        # 2. Contextual Summary
        kr_bullets = self._generate_korean_bullets(title, summary, category_name)
        article["summary_bullets_kr"] = kr_bullets

        return article

    def summarize_all(self, articles: List[Dict[str, any]], max_workers: int = 8) -> List[Dict[str, any]]:
        """Summarize and translate all articles concurrently for fast execution."""
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            summarized_list = list(executor.map(self.summarize_article, articles))

        return summarized_list

    def generate_executive_briefing(self, articles: List[Dict[str, any]]) -> Dict[str, any]:
        """Generate comprehensive executive team briefing with schedule and official injury table."""
        schedule_data = self.schedule_manager.get_schedule_data(articles)
        injury_table_data = self.injury_tracker.get_injury_report_table(articles)

        if not articles:
            return {
                "headline": "수집된 Chargers 뉴스가 없습니다.",
                "key_takeaways": [],
                "injury_update": "특이사항 없음",
                "team_outlook": "최신 뉴스를 업데이트해 주세요.",
                "game_center": {},
                "schedule": schedule_data,
                "injury_report_table": injury_table_data,
                "trending_keywords": [],
                "top_highlights": [],
            }

        game_data = self.game_analyzer.analyze_game_news(articles)
        trend_data = self.keyword_tracker.extract_trends_from_articles(articles)
        top_highlights = self.ranker.get_top_priority(articles, limit=5)

        briefing = self._generate_heuristic_briefing(articles, game_data, trend_data)
        briefing["game_center"] = game_data
        briefing["schedule"] = schedule_data
        briefing["injury_report_table"] = injury_table_data
        briefing["trending_keywords"] = trend_data.get("trending_keywords", [])
        briefing["top_highlights"] = top_highlights
        return briefing

    def _generate_korean_bullets(self, title: str, summary: str, category_name: str) -> List[str]:
        """Generate fluent, readable Korean bullet points focusing on context and impact."""
        bullets = []
        text = f"{title}. {summary}"
        lower_text = text.lower()

        # 1. Main Core Story Paragraph
        clean_sum = re.sub(r"<[^>]+>", "", summary).strip() if summary else ""
        is_boilerplate = (
            "submitted by" in clean_sum.lower()
            or "[link]" in clean_sum.lower()
            or "[comments]" in clean_sum.lower()
            or len(clean_sum) < 25
        )

        if clean_sum and not is_boilerplate:
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_sum) if len(s.strip()) > 15]
            raw_text = " ".join(sentences[:2]) if len(sentences) > 1 else (sentences[0] if sentences else clean_sum)
            if len(raw_text) > 250:
                raw_text = raw_text[:247] + "..."

            translated = self.translator.translate_text(raw_text, max_chars=250)
            bullets.append(f"⚡ **핵심 소식**: {translated}")
        else:
            clean_title = re.sub(r"\[.*?\]", "", title).strip() or title
            translated_title = self.translator.translate_text(clean_title, max_chars=180)
            bullets.append(f"⚡ **핵심 소식**: {translated_title}")

        # 2. Team Impact / Tactical Context
        involved = []
        for name, en_label in KEY_PLAYERS_EN.items():
            pattern = r"\b" + re.escape(name) + r"\b"
            if re.search(pattern, lower_text):
                involved.append(en_label)

        if involved:
            players_str = ", ".join(involved[:2])
            if "injury" in lower_text or "ankle" in lower_text or "knee" in lower_text or "ir" in lower_text:
                bullets.append(f"📋 **선수단 영향**: {players_str}의 부상 경과 및 훈련 소화 여부가 주간 라인업 구성의 핵심 변수로 작용합니다.")
            elif "roster" in lower_text or "53-man" in lower_text or "sign" in lower_text or "cut" in lower_text:
                bullets.append(f"📋 **로스터 분석**: {players_str} 관련 뎁스 차트 변동으로 팀 전력 구성에 변화가 생겼습니다.")
            elif "harbaugh" in lower_text or "coach" in lower_text:
                bullets.append(f"🏈 **전술 관전 포인트**: Jim Harbaugh 감독 및 코칭스태프의 피지컬 중심 미식축구 철학이 반영된 행보입니다.")
            else:
                bullets.append(f"🏈 **주요 인물**: {players_str}의 경기력과 훈련 컨디션이 집중 조명되고 있습니다.")

        return bullets[:2]

    def _generate_heuristic_briefing(
        self,
        articles: List[Dict[str, any]],
        game_data: Dict[str, any],
        trend_data: Dict[str, any],
    ) -> Dict[str, any]:
        """Create a structured executive briefing in Korean with English proper nouns."""
        total_count = len(articles)

        player_counts: Dict[str, int] = {}
        for art in articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
            for p, en_label in KEY_PLAYERS_EN.items():
                pattern = r"\b" + re.escape(p) + r"\b"
                if re.search(pattern, text):
                    player_counts[en_label] = player_counts.get(en_label, 0) + 1

        top_players = sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_players_str = ", ".join([f"{p}({c}건)" for p, c in top_players]) if top_players else "선수단 전원"

        headline = f"⚡ LA Chargers 주간 인텔리전스 종합 리포트 (총 {total_count}건 정밀 분석)"

        takeaways = [
            f"⚡ **스마트 큐레이션 및 중복 제거**: 총 {total_count}건의 언론 기사를 정밀 클러스터링하여 핵심 이슈 위주로 요약했습니다.",
            f"🏈 **매치업 포커스**: {game_data.get('game_type', '정규시즌 경기')} (상대: {game_data.get('opponent', '미정')})",
            f"🎯 **집중 조명된 핵심 인물**: {top_players_str}",
            f"🔥 **헤드라인 키워드**: {', '.join(trend_data.get('trending_keywords', [])[:4]) if trend_data.get('trending_keywords') else 'Justin Herbert, Jim Harbaugh'}",
        ]

        injury_str = "부상 리포트 공식 테이블(Injury Report Table)에서 상세 출전 상태 및 연습 참가 여부(DNP/LP/FP)를 확인하세요."

        return {
            "headline": headline,
            "key_takeaways": takeaways,
            "injury_update": injury_str,
            "team_outlook": "Jim Harbaugh 감독 체제 하에서 공수 밸런스와 오펜시브 라인의 견고함을 구축하며 시즌 순항 중입니다.",
        }
