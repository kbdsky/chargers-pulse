"""Game and Matchup Intelligence Analyzer for Chargers (Precise Matchup Detection & Professional Sports Analysis)."""

import re
from typing import Dict, List, Optional
from ..config import NFL_TEAMS


class GameAnalyzer:
    """Analyzes game results, upcoming matchups, opponents, scores, and tactical takeaways."""

    def analyze_game_news(self, articles: List[Dict[str, any]]) -> Dict[str, any]:
        """Synthesize game-specific news and match intelligence with strict accuracy."""
        # 1. Filter only professional sports media articles (exclude reddit/community posts)
        valid_game_articles = []
        for art in articles:
            source = art.get("source", "").lower()
            title = art.get("title", "").lower()
            summary = art.get("summary", "").lower()

            # Skip reddit or forum threads for official game center
            if "reddit" in source or "tailgate" in title or "buy/sell" in title:
                continue

            # Must be game-related
            is_game = (
                art.get("category_key") == "game"
                or "vs" in title
                or "recap" in title
                or "week 1" in title
                or "opener" in title
                or "game" in title
                or "matchup" in title
            )
            if is_game:
                valid_game_articles.append(art)

        # Sort by published date descending (newest first)
        valid_game_articles.sort(key=lambda x: x.get("published", ""), reverse=True)

        if not valid_game_articles:
            return {
                "has_game_data": False,
                "opponent": "Las Vegas Raiders (LV Raiders)",
                "game_type": "정규시즌 1주차 개막전",
                "score_detected": "킥오프 대기 (개막전 프리뷰)",
                "highlights": ["현재 정규시즌 1주차 개막전 대비 훈련 및 전술 점검이 진행 중입니다."],
                "offense_notes": "QB Justin Herbert 중심의 패싱 전술과 Joe Alt, Rashawn Slater의 든든한 태클 라인 프로텍션",
                "defense_notes": "Jesse Minter 수비 코디네이터 체제 하에서 Joey Bosa, Khalil Mack의 강력한 패스 러시",
            }

        # 2. Determine current match stage (Upcoming Week 1 vs Recent Recap)
        is_week1_upcoming = False
        latest_opponent = "Las Vegas Raiders (LV Raiders)"
        game_status = "킥오프 예정 (개막전 프리뷰)"
        game_type = "정규시즌 1주차 개막전"

        # Check newest 5 articles
        for art in valid_game_articles[:5]:
            t = art.get("title", "").lower()
            if "week 1" in t or "opener" in t or "ahead of week" in t:
                is_week1_upcoming = True
                break

        if is_week1_upcoming:
            game_type = "정규시즌 1주차 개막전"
            game_status = "킥오프 대기 (정규시즌 개막전)"
            latest_opponent = "Las Vegas Raiders (LV Raiders)"
        else:
            # Check for latest game recap
            for art in valid_game_articles:
                t = art.get("title", "").lower()
                if "recap" in t or "final" in t or "fall to" in t or "roll past" in t:
                    # Detect opponent in title
                    for opp_key, opp_val in NFL_TEAMS.items():
                        if opp_key in t:
                            latest_opponent = opp_val
                            break
                    scores = re.findall(r"\b\d{1,2}\s*-\s*\d{1,2}\b", art.get("title", "") + " " + art.get("summary", ""))
                    if scores:
                        game_status = f"최근 경기 결과 ({scores[0]})"
                    else:
                        game_status = "최근 경기 종료"
                    game_type = "프리시즌 경기 결과" if "preseason" in t else "정규시즌 경기 결과"
                    break

        # 3. Curate clean, high-quality highlights from verified media
        highlights = []
        for art in valid_game_articles[:4]:
            t = art.get("headline_kr") or art.get("title", "")
            bullets = art.get("summary_bullets_kr", [])
            b_text = bullets[0] if bullets else art.get("summary", "")[:80] + "..."
            # Clean formatting
            b_text_clean = b_text.replace("📌 **핵심 요약:**", "").strip()
            highlights.append(f"🏈 **{t}**: {b_text_clean}")

        return {
            "has_game_data": True,
            "opponent": latest_opponent,
            "game_type": game_type,
            "score_detected": game_status,
            "game_articles_count": len(valid_game_articles),
            "highlights": highlights,
            "offense_notes": "QB Justin Herbert의 정교한 딥패스와 Joe Alt, Rashawn Slater의 오펜시브 라인 프로텍션 집중",
            "defense_notes": "Jesse Minter 수비 코디네이터 지휘 아래 Joey Bosa, Khalil Mack의 엣지 러시 및 Derwin James Jr.의 세컨더리 지휘",
        }
