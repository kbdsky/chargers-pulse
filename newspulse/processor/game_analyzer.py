"""Game and Matchup Intelligence Analyzer for Chargers (2026 Season Schedule & Real-Time Opponent Detection)."""

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
                or "cardinals" in title
            )
            if is_game:
                valid_game_articles.append(art)

        # Sort by published date descending (newest first)
        valid_game_articles.sort(key=lambda x: x.get("published", ""), reverse=True)

        if not valid_game_articles:
            return {
                "has_game_data": False,
                "opponent": "Denver Broncos (DEN Broncos)",
                "game_type": "2026 정규시즌 5주차 (SoFi Stadium / 디비전 라이벌전)",
                "score_detected": "킥오프 대기 (5주차 덴버전 프리뷰)",
                "highlights": ["현재 정규시즌 5주차 Denver Broncos와의 AFC West 홈경기 대비 훈련 및 전술 점검이 진행 중입니다."],
                "offense_notes": "Jim Harbaugh 감독과 Mike McDaniel OC 체제 하에서 QB Justin Herbert 중심의 패싱 전술 및 턴오버 억제",
                "defense_notes": "Chris O'Leary 수비 코디네이터 지휘 아래 Khalil Mack, Tuli Tuipulotu, Bud Dupree의 강력한 엣지 패스 러시 가동",
            }

        # 2. Determine current opponent and matchup based on mention frequency
        opp_counts = {}
        for art in valid_game_articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
            for opp_key, opp_val in NFL_TEAMS.items():
                if opp_key in ["chargers", "los angeles", "la"]:
                    continue
                if re.search(r"\b" + re.escape(opp_key) + r"\b", text):
                    opp_counts[opp_val] = opp_counts.get(opp_val, 0) + 1

        # Check upcoming game from schedule
        sched_next_opp = None
        try:
            from .schedule_manager import ScheduleManager
            sched = ScheduleManager().get_schedule_data()
            sched_next_opp = sched.get("next_game", {}).get("opponent")
        except Exception:
            pass

        latest_opponent = None
        if sched_next_opp and opp_counts:
            clean_next = sched_next_opp.lower()
            for opp_val in opp_counts.keys():
                if any(part in clean_next for part in opp_val.lower().split() if len(part) > 3):
                    latest_opponent = sched_next_opp
                    break

        if not latest_opponent:
            if opp_counts:
                latest_opponent = max(opp_counts.items(), key=lambda x: x[1])[0]
            elif sched_next_opp:
                latest_opponent = sched_next_opp
            else:
                latest_opponent = "Denver Broncos (DEN Broncos)"

        if "broncos" in latest_opponent.lower():
            game_type = "2026 정규시즌 5주차 (SoFi Stadium / AFC West 디비전 라이벌전)"
            game_status = "킥오프 대기 (5주차 덴버 브롱코스 홈경기)"
            offense_notes = "개막 4연패 탈출이 걸린 Jim Harbaugh호와 Mike McDaniel OC 공격진. 양쪽 주전 태클 Joe Alt·Rashawn Slater가 목요일까지 훈련 불참(DNP)해 패스 프로텍션이 최대 변수 (4주차 Justin Herbert 피색 4회)"
            defense_notes = "Chris O'Leary 수비 코디네이터 체제에서 QB Bo Nix가 이끄는 Broncos 공격 봉쇄. 세컨더리 Derwin James Jr.·Donte Jackson이 목요일까지 DNP로 출전 여부 미정"
            highlights = [
                "🏈 **2026 NFL 5주차 홈 맞대결**: 10월 11일(현지) SoFi Stadium, Denver Broncos와의 AFC West 디비전 라이벌전 (CBS)",
                "🔥 **시즌 첫 승 도전**: 0승 4패로 AFC West 최하위, 연패 탈출이 걸린 경기",
                "🏈 **공격 관전 포인트**: 주전 태클 공백 가능성 속 Mike McDaniel OC의 퀵 패스·보호 전략",
                "🩹 **부상 변수**: 금요일 최종 부상 리포트에서 Joe Alt·Rashawn Slater·Derwin James Jr.·Ladd McConkey의 출전 지정 확정 예정",
            ]
        elif "seahawks" in latest_opponent.lower():
            game_type = "2026 정규시즌 4주차 (Lumen Field / NFC 원정)"
            game_status = "23 - 30 (패배)"
            offense_notes = "Justin Herbert 19/31, 189야드, 1TD 2INT, 피색 4회. 전반 6-20으로 끌려간 뒤 후반 추격했으나 마지막 공격에서 스트립 색으로 펌블"
            defense_notes = "전반에만 20실점, 3쿼터 초반 6-27까지 벌어지며 초반 실점이 패인"
            highlights = [
                "🏈 **2026 NFL 4주차 경기 결과**: Seattle Seahawks에 23-30 패배 (시즌 0승 4패)",
                "🏈 **경기 흐름**: 전반 6-20, 3쿼터 6-27 열세에서 23-30까지 추격했으나 종료 2분여 전 Herbert가 Uchenna Nwosu에게 스트립 색을 당해 패배 확정",
            ]
        elif "bills" in latest_opponent.lower():
            game_type = "2026 정규시즌 3주차 (Highmark Stadium)"
            game_status = "16 - 24 (패배)"
            offense_notes = "QB Justin Herbert 중심의 패싱 전술과 오펜시브 라인 수호"
            defense_notes = "Chris O'Leary 수비 코디네이터 지휘 아래 Buffalo Bills 봉쇄 시도 및 수비진 분전"
            highlights = [
                "🏈 **2026 NFL 3주차 경기 결과**: Buffalo Bills에 16-24 패배 (시즌 0승 3패)",
            ]
        elif "raiders" in latest_opponent.lower():
            game_type = "2026 정규시즌 2주차 (SoFi Stadium / AFC West 라이벌전)"
            game_status = "14 - 26 (패배)"
            offense_notes = "QB Justin Herbert 중심의 패싱 전술과 태클 프로텍션"
            defense_notes = "Khalil Mack, Tuli Tuipulotu, Bud Dupree의 엣지 압박 및 Derwin James Jr.의 수비 조율"
            highlights = [
                "🏈 **2026 NFL 2주차 경기 결과**: Las Vegas Raiders에 14-26 패배 (시즌 0승 2패)",
                "🏈 **Jim Harbaugh 감독 체제 점검**: 턴오버 억제 및 공격 전술 재정비 필요",
            ]
        elif "cardinals" in latest_opponent.lower():
            game_type = "2026 정규시즌 1주차 (SoFi Stadium)"
            game_status = "14 - 26 (패배)"
            offense_notes = "QB Justin Herbert 중심의 패싱 전술과 오펜시브 라인 프로텍션"
            defense_notes = "Chris O'Leary 수비 코디네이터 지휘 아래 Khalil Mack, Tuli Tuipulotu의 엣지 러시 및 수비진 조직력"
            highlights = [
                "🏈 **2026 NFL 1주차 경기 결과**: Arizona Cardinals에 14-26 패배",
                "🏈 **Jim Harbaugh 감독 체제 점검**: 오펜스 라인 및 수비진 조직력 재정비 필요",
            ]
        else:
            game_type = f"2026 시즌 경기 (상대: {latest_opponent})"
            game_status = "경기 프리뷰"
            offense_notes = "QB Justin Herbert 중심의 패싱 전술과 오펜시브 라인 프로텍션"
            defense_notes = "Chris O'Leary 수비 코디네이터 지휘 아래 Khalil Mack 중심의 패스 러시 및 세컨더리 압박"
            highlights = [
                f"🏈 **{latest_opponent} 맞대결**: 팀 전력 및 주요 전술 점검",
            ]

        # Detect score ONLY if current matchup is not an upcoming kickoff wait
        if "킥오프 대기" not in game_status:
            for art in valid_game_articles:
                text = f"{art.get('title', '')} {art.get('summary', '')}"
                score_match = re.search(r"\b(\d{1,2})\s*[-–]\s*(\d{1,2})\b", text)
                if score_match and ("final" in text.lower() or "win" in text.lower() or "loss" in text.lower() or "recap" in text.lower()):
                    game_status = f"{score_match.group(1)}-{score_match.group(2)}"
                    break

        return {
            "has_game_data": True,
            "opponent": latest_opponent,
            "game_type": game_type,
            "score_detected": game_status,
            "game_articles_count": len(valid_game_articles),
            "highlights": highlights,
            "offense_notes": offense_notes,
            "defense_notes": defense_notes,
        }
