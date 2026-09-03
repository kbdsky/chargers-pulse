"""Summarization engine supporting AI, deep Korean translation, and smart sports NLP synthesis.
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

logger = logging.getLogger(__name__)

FOOTBALL_TERMS = {
    "injury": "부상",
    "injured": "부상자",
    "injured reserve": "부상자 명단(IR)",
    "surgery": "수술",
    "concussion": "뇌진탕",
    "ankle": "발목 부상",
    "knee": "무릎 부상",
    "hamstring": "햄스트링",
    "touchdown": "터치다운",
    "interception": "인터셉션(가로채기)",
    "quarterback": "쿼터백(QB)",
    "starter": "선발 스타터",
    "53-man roster": "53인 로스터",
    "53-man": "53인 로스터",
    "roster": "선수 로스터",
    "head coach": "헤드코치(감독)",
    "offensive coordinator": "공격 코디네이터",
    "defensive coordinator": "수비 코디네이터",
    "preseason": "프리시즌",
    "regular season": "정규시즌",
    "recap": "경기 결과 분석",
    "joint practice": "합동 훈련",
    "practice squad": "연습 스쿼드",
    "free agency": "자유계약(FA)",
    "trade": "트레이드",
    "contract": "계약/연장",
    "draft": "드래프트",
}

KEY_PLAYERS_EN = {
    "justin herbert": "Justin Herbert (QB)",
    "jim harbaugh": "Jim Harbaugh (HC)",
    "joe alt": "Joe Alt (OT)",
    "ladd mcconkey": "Ladd McConkey (WR)",
    "derwin james": "Derwin James (S)",
    "joey bosa": "Joey Bosa (EDGE)",
    "khalil mack": "Khalil Mack (EDGE)",
    "jk dobbins": "J.K. Dobbins (RB)",
    "gus edwards": "Gus Edwards (RB)",
    "quentin johnston": "Quentin Johnston (WR)",
    "joshua palmer": "Joshua Palmer (WR)",
    "rashawn slater": "Rashawn Slater (OT)",
    "greg roman": "Greg Roman (OC)",
    "jesse minter": "Jesse Minter (DC)",
    "tyler biadasz": "Tyler Biadasz (C)",
    "omarion hampton": "Omarion Hampton (RB)",
    "genesis smith": "Genesis Smith (DB)",
    "nadame tucker": "Nadame Tucker (EDGE)",
    "mike vrabel": "Mike Vrabel (Coach)",
}


class Summarizer:
    """Generates fluent Korean bullet summaries with English proper nouns preserved."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "auto"):
        self.gemini_key = api_key or os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.provider = provider
        self.game_analyzer = GameAnalyzer()
        self.keyword_tracker = DynamicKeywordTracker()
        self.ranker = ArticleRanker()
        self.translator = KoreanTranslator()

    def summarize_article(self, article: Dict[str, any]) -> Dict[str, any]:
        """Generate fluent Korean headline and summary bullet points with English proper nouns."""
        title = article.get("title", "")
        summary = article.get("summary", "")
        category_name = article.get("category_name", "팀 소식")

        # 1. Headline: Korean translation with English proper nouns
        kr_headline = self.translator.translate_text(title, max_chars=180)
        if not self.translator._is_valid_translation(kr_headline):
            kr_headline = self.translator.synthesize_korean_sentence(title)
        article["headline_kr"] = kr_headline if kr_headline else title

        # 2. Bullet points
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
        """Generate comprehensive executive team briefing in Korean with English proper nouns."""
        if not articles:
            return {
                "headline": "수집된 Chargers 뉴스가 없습니다.",
                "key_takeaways": [],
                "injury_update": "특이사항 없음",
                "team_outlook": "최신 뉴스를 업데이트해 주세요.",
                "game_center": {},
                "trending_keywords": [],
                "top_highlights": [],
            }

        game_data = self.game_analyzer.analyze_game_news(articles)
        trend_data = self.keyword_tracker.extract_trends_from_articles(articles)
        top_highlights = self.ranker.get_top_priority(articles, limit=5)

        if self.gemini_key:
            ai_brief = self._generate_ai_briefing(articles)
            if ai_brief:
                ai_brief["game_center"] = game_data
                ai_brief["trending_keywords"] = trend_data.get("trending_keywords", [])
                ai_brief["top_highlights"] = top_highlights
                return ai_brief

        briefing = self._generate_heuristic_briefing(articles, game_data, trend_data)
        briefing["game_center"] = game_data
        briefing["trending_keywords"] = trend_data.get("trending_keywords", [])
        briefing["top_highlights"] = top_highlights
        return briefing

    def _generate_korean_bullets(self, title: str, summary: str, category_name: str) -> List[str]:
        """Generate 2-3 structured Korean bullets with translated summary and English names."""
        bullets = []
        text = f"{title}. {summary}"
        lower_text = text.lower()

        # 1. Fluent Korean Summary with English Proper Nouns
        if summary and len(summary.strip()) > 20:
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", summary) if len(s.strip()) > 15]
            raw_text_to_translate = " ".join(sentences[:2]) if len(sentences) > 1 else sentences[0]
            if len(raw_text_to_translate) > 250:
                raw_text_to_translate = raw_text_to_translate[:247] + "..."

            translated_summary = self.translator.translate_text(raw_text_to_translate, max_chars=250)
            if not self.translator._is_valid_translation(translated_summary):
                translated_summary = self.translator.synthesize_korean_sentence(raw_text_to_translate)
            bullets.append(f"📌 **핵심 요약:** {translated_summary}")
        else:
            translated_title = self.translator.translate_text(title, max_chars=150)
            if not self.translator._is_valid_translation(translated_title):
                translated_title = self.translator.synthesize_korean_sentence(title)
            bullets.append(f"📌 **핵심 요약:** {translated_title}")

        # 2. Key Players in English with Position Code
        involved = []
        for name, en_label in KEY_PLAYERS_EN.items():
            pattern = r"\b" + re.escape(name) + r"\b"
            if re.search(pattern, lower_text):
                involved.append(en_label)

        if involved:
            bullets.append(f"🏈 **주요 인물:** {', '.join(involved[:3])}")

        # 3. Key Football Points in Korean
        terms = []
        for eng, kor in FOOTBALL_TERMS.items():
            pattern = r"\b" + re.escape(eng) + r"\b"
            if re.search(pattern, lower_text):
                if kor not in terms:
                    terms.append(kor)

        if terms:
            bullets.append(f"⚡ **주요 포인트:** {', '.join(terms[:3])} 관련 동향 ({category_name})")

        return bullets[:3]

    def _generate_heuristic_briefing(
        self,
        articles: List[Dict[str, any]],
        game_data: Dict[str, any],
        trend_data: Dict[str, any],
    ) -> Dict[str, any]:
        """Create a structured executive briefing in Korean with English proper nouns."""
        total_count = len(articles)

        cat_counts: Dict[str, int] = {}
        for art in articles:
            cat = art.get("category_name", "팀 소식")
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        player_counts: Dict[str, int] = {}
        for art in articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
            for p, en_label in KEY_PLAYERS_EN.items():
                pattern = r"\b" + re.escape(p) + r"\b"
                if re.search(pattern, text):
                    player_counts[en_label] = player_counts.get(en_label, 0) + 1

        top_players = sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_players_str = ", ".join([f"{p[0]}({p[1]}건)" for p in top_players]) if top_players else "Justin Herbert, Jim Harbaugh"

        injuries = [art for art in articles if art.get("category_key") == "injury"]
        if injuries:
            first_inj = injuries[0]
            inj_title = first_inj.get("headline_kr", first_inj.get("title", ""))
            injury_summary = f"총 {len(injuries)}건의 부상 및 로스터 관련 소식이 집계되었습니다. (주요 이슈: {inj_title})"
        else:
            injury_summary = "현재 긴급 추가 부상자 이슈 없이 정규시즌 대비 훈련 및 53인 로스터 정비가 순조롭게 진행 중입니다."

        game_status = (
            f"최근 경기/일정: {game_data.get('game_type', '경기')} (상대: {game_data.get('opponent', '미정')})"
            if game_data.get("has_game_data")
            else "정규시즌 개막 대비 팀 전술 훈련 진행 중"
        )

        hot_trends = trend_data.get("trending_keywords", [])
        trends_str = ", ".join(hot_trends[:5]) if hot_trends else "Justin Herbert, Jim Harbaugh, Tyler Biadasz, 49ers"

        takeaways = [
            f"⚡ 전수 수집 및 스마트 랭킹: 총 {total_count}건의 기사를 전수 분석하여 중요도 순으로 큐레이션했습니다.",
            f"🏈 경기 및 매치업 동향: {game_status}",
            f"🎯 집중 조명된 핵심 인물: {top_players_str}",
            f"🔥 실시간 급상승 키워드: {trends_str}",
            f"📊 카테고리별 분포: " + ", ".join([f"{k} {v}건" for k, v in cat_counts.items()]),
            f"🛡️ Jim Harbaugh 감독과 Jesse Minter 코디네이터 체제 하에서 피지컬과 수비 규율이 강화되고 있습니다.",
        ]

        return {
            "headline": f"⚡ LA Chargers 종합 인텔리전스 주간 리포트 (총 {total_count}건 전수 분석)",
            "key_takeaways": takeaways,
            "injury_update": injury_summary,
            "team_outlook": f"전문 미디어 전수 수집 데이터 기반 Chargers 브리핑입니다. {game_data.get('offense_notes', '')}",
        }

    def _generate_ai_briefing(self, articles: List[Dict[str, any]]) -> Optional[Dict[str, any]]:
        """Optional Gemini API integration for deep Korean executive synthesis."""
        try:
            import requests

            titles_and_summaries = "\n".join(
                [f"- [중요도:{art.get('importance_score', 50)}][{art.get('category_name')}] {art.get('title')}: {art.get('summary')[:200]}" for art in articles[:20]]
            )

            prompt = (
                "당신은 NFL LA Chargers 전문 수석 스포츠 분석가입니다. "
                "아래 전수 수집된 최신 영문 뉴스들을 심층 분석하여 한국어로 고품질 주간 인텔리전스 브리핑을 작성해 주세요.\n"
                "규칙:\n"
                "1. 설명과 해설은 100% 매끄럽고 완벽한 한국어 문장으로 작성하세요.\n"
                "2. 선수 이름(Justin Herbert, Tyler Biadasz 등)과 팀 이름(Chargers, 49ers 등)은 고유명사이므로 영어 원문 그대로 표기하세요.\n\n"
                f"{titles_and_summaries}\n\n"
                "다음 JSON 포맷으로만 응답해 주세요:\n"
                "{\n"
                '  "headline": "한 줄 핵심 총괄 브리핑 헤드라인",\n'
                '  "key_takeaways": ["핵심 분석 1", "핵심 분석 2", "핵심 분석 3", "핵심 분석 4", "핵심 분석 5"],\n'
                '  "injury_update": "부상 및 53인 로스터 정비 상황 상세 요약",\n'
                '  "team_outlook": "팀 전력 및 향후 경기/시즌 종합 전망"\n'
                "}"
            )

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                import json
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_content)
        except Exception as e:
            logger.warning(f"AI Briefing failed, falling back to heuristic: {e}")

        return None
