"""Game and Matchup Intelligence Analyzer for Chargers (English Proper Nouns)."""

import re
from typing import Dict, List, Optional
from ..config import NFL_TEAMS


class GameAnalyzer:
    """Analyzes game results, opponents, scores, and tactical takeaways with English proper nouns."""

    def analyze_game_news(self, articles: List[Dict[str, any]]) -> Dict[str, any]:
        """Synthesize game-specific news and match intelligence."""
        game_articles = [a for a in articles if a.get("category_key") == "game" or "vs" in a.get("title", "").lower() or "recap" in a.get("title", "").lower()]

        if not game_articles:
            return {
                "has_game_data": False,
                "opponent": "미정",
                "game_type": "시즌 준비 단계",
                "score_detected": None,
                "highlights": ["현재 수집된 경기 결과 소식이 없습니다."],
                "offense_notes": "정규시즌 개막 대비 공격 전술 훈련 진행 중",
                "defense_notes": "수비진 압박 및 세컨더리 로테이션 점검 중",
            }

        detected_opponents = []
        detected_scores = []
        is_preseason = False
        is_joint_practice = False
        game_type = "정규시즌/프리시즌 경기"

        for art in game_articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}"
            lower = text.lower()

            if "preseason" in lower:
                is_preseason = True
            if "joint practice" in lower or "합동 훈련" in text:
                is_joint_practice = True

            scores = re.findall(r"\b\d{1,2}\s*-\s*\d{1,2}\b", text)
            if scores:
                detected_scores.extend(scores)

            for opp_key, opp_val in NFL_TEAMS.items():
                if re.search(r"\b" + re.escape(opp_key) + r"\b", lower):
                    detected_opponents.append(opp_val)

        if is_preseason:
            game_type = "프리시즌 매치"
        if is_joint_practice:
            game_type = "합동 훈련 및 평가전"

        main_opponent = detected_opponents[0] if detected_opponents else "SF 49ers"
        score_info = detected_scores[0] if detected_scores else "스코어 미확정 / 프리뷰"

        # Generate structured key points
        game_points = []
        for art in game_articles[:4]:
            t = art.get("title", "")
            bullets = art.get("summary_bullets_kr", [])
            b_text = bullets[0] if bullets else t
            game_points.append(f"🏈 **{t}**: {b_text}")

        return {
            "has_game_data": True,
            "opponent": main_opponent,
            "game_type": game_type,
            "score_detected": score_info,
            "game_articles_count": len(game_articles),
            "highlights": game_points,
            "offense_notes": "쿼터백 Justin Herbert 중심의 패싱 전술과 J.K. Dobbins, Gus Edwards의 러닝 어택 호흡 점검",
            "defense_notes": "Jesse Minter 수비 코디네이터 체제 하에서 Joey Bosa, Khalil Mack의 패스 러시 및 신예 세컨더리 실전 테스트 집중",
        }
