"""2026 LA Chargers NFL Schedule & Match Intelligence Manager with KST Time Conversion."""

import re
import datetime
from typing import Dict, List, Optional


CHARGERS_2026_SCHEDULE = [
    {
        "week": 1,
        "date_utc": "2026-09-13T20:05:00Z",
        "date_kst": "2026년 9월 14일 (월) 오전 05:05 (KST)",
        "opponent": "Arizona Cardinals (AZ Cardinals)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 1주차 홈 개막전",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 2,
        "date_utc": "2026-09-20T20:05:00Z",
        "date_kst": "2026년 9월 21일 (월) 오전 05:05 (KST)",
        "opponent": "Las Vegas Raiders (LV Raiders)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 2주차 (AFC West 라이벌전)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 3,
        "date_utc": "2026-09-27T20:25:00Z",
        "date_kst": "2026년 9월 28일 (월) 오전 05:25 (KST)",
        "opponent": "Kansas City Chiefs (KC Chiefs)",
        "is_home": False,
        "stadium": "GEHA Field at Arrowhead (Kansas City, MO)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 3주차 (지구 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 4,
        "date_utc": "2026-10-04T20:05:00Z",
        "date_kst": "2026년 10월 5일 (월) 오전 05:05 (KST)",
        "opponent": "Denver Broncos (DEN Broncos)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 4주차 (지구 홈경기)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 5,
        "date_utc": "2026-10-11T20:25:00Z",
        "date_kst": "2026년 10월 12일 (월) 오전 05:25 (KST)",
        "opponent": "Dallas Cowboys (DAL Cowboys)",
        "is_home": False,
        "stadium": "AT&T Stadium (Arlington, TX)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 5주차 (NFC 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 6,
        "date_utc": "2026-10-18T20:05:00Z",
        "date_kst": "2026년 10월 19일 (월) 오전 05:05 (KST)",
        "opponent": "New York Giants (NY Giants)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 6주차 홈경기",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 7,
        "date_utc": "2026-10-25T20:05:00Z",
        "date_kst": "2026년 10월 26일 (월) 오전 05:05 (KST)",
        "opponent": "Las Vegas Raiders (LV Raiders)",
        "is_home": False,
        "stadium": "Allegiant Stadium (Las Vegas, NV)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 7주차 (라베 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 8,
        "date_utc": "2026-11-01T21:25:00Z",
        "date_kst": "2026년 11월 2일 (월) 오전 06:25 (KST)",
        "opponent": "Philadelphia Eagles (PHI Eagles)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 8주차 홈경기",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 9,
        "date_utc": None,
        "date_kst": "2026년 11월 9일 주간",
        "opponent": "BYE WEEK (휴식 주간)",
        "is_home": True,
        "stadium": "-",
        "broadcast": "-",
        "game_type": "바이 위크 (선수단 휴식 및 재정비)",
        "status": "bye",
        "score": "-",
        "result": "-",
    },
    {
        "week": 10,
        "date_utc": "2026-11-15T21:05:00Z",
        "date_kst": "2026년 11월 16일 (월) 오전 06:05 (KST)",
        "opponent": "Denver Broncos (DEN Broncos)",
        "is_home": False,
        "stadium": "Empower Field at Mile High (Denver, CO)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 10주차 (덴버 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 11,
        "date_utc": "2026-11-22T21:25:00Z",
        "date_kst": "2026년 11월 23일 (월) 오전 06:25 (KST)",
        "opponent": "Kansas City Chiefs (KC Chiefs)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 11주차 (치프스 홈 리턴매치)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 12,
        "date_utc": "2026-11-29T18:00:00Z",
        "date_kst": "2026년 11월 30일 (월) 오전 03:00 (KST)",
        "opponent": "Washington Commanders (WAS Commanders)",
        "is_home": False,
        "stadium": "Northwest Stadium (Landover, MD)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 12주차 (워싱턴 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 13,
        "date_utc": "2026-12-06T21:05:00Z",
        "date_kst": "2026년 12월 7일 (월) 오전 06:05 (KST)",
        "opponent": "Seattle Seahawks (SEA Seahawks)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 13주차 홈경기",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 14,
        "date_utc": "2026-12-13T21:25:00Z",
        "date_kst": "2026년 12월 14일 (월) 오전 06:25 (KST)",
        "opponent": "San Francisco 49ers (SF 49ers)",
        "is_home": False,
        "stadium": "Levi's Stadium (Santa Clara, CA)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 14주차 (캘리포니아 라이벌전)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 15,
        "date_utc": "2026-12-20T21:05:00Z",
        "date_kst": "2026년 12월 21일 (월) 오전 06:05 (KST)",
        "opponent": "Los Angeles Rams (LA Rams)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 15주차 (LA 더비)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 16,
        "date_utc": "2026-12-27T18:00:00Z",
        "date_kst": "2026년 12월 28일 (월) 오전 03:00 (KST)",
        "opponent": "Houston Texans (HOU Texans)",
        "is_home": False,
        "stadium": "NRG Stadium (Houston, TX)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 16주차 (휴스턴 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 17,
        "date_utc": "2027-01-03T18:00:00Z",
        "date_kst": "2027년 1월 4일 (월) 오전 03:00 (KST)",
        "opponent": "New England Patriots (NE Patriots)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 17주차 홈 최종전",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 18,
        "date_utc": "2027-01-10T21:25:00Z",
        "date_kst": "2027년 1월 11일 (월) 오전 06:25 (KST)",
        "opponent": "Las Vegas Raiders (LV Raiders)",
        "is_home": False,
        "stadium": "Allegiant Stadium (Las Vegas, NV)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 18주차 최종전",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
]


class ScheduleManager:
    """Manages the 2026 Chargers schedule with KST kickoffs, live statuses, and automatic result updates."""

    def __init__(self):
        pass

    def get_schedule_data(self, articles: List[Dict[str, any]] = None) -> Dict[str, any]:
        """Generate structured schedule data with KST times, next game highlights, and dynamic results."""
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        schedule_list = [dict(item) for item in CHARGERS_2026_SCHEDULE]

        wins = 0
        losses = 0
        ties = 0
        next_game = None

        # Process each game
        for item in schedule_list:
            if item.get("status") == "bye" or not item.get("date_utc"):
                continue

            try:
                game_time_utc = datetime.datetime.fromisoformat(item["date_utc"].replace("Z", "+00:00"))
                diff_seconds = (game_time_utc - now_utc).total_seconds()

                if diff_seconds > 0:
                    # Upcoming game
                    days_left = int(diff_seconds // 86400)
                    hours_left = int((diff_seconds % 86400) // 3600)

                    if days_left == 0:
                        d_day_str = f"오늘 킥오프 ({hours_left}시간 남음)"
                    elif days_left == 1:
                        d_day_str = "내일 킥오프 (D-1)"
                    else:
                        d_day_str = f"D-{days_left}"

                    item["status"] = "upcoming"
                    item["d_day"] = d_day_str

                    if next_game is None:
                        next_game = item
                else:
                    # Past game - Check for final score from collected articles
                    item["status"] = "final"
                    item["d_day"] = "경기 종료"

                    # Scan articles for game score if available
                    score, result = self._detect_game_result(item, articles or [])
                    if score:
                        item["score"] = score
                        item["result"] = result
                        if result == "WIN":
                            wins += 1
                        elif result == "LOSS":
                            losses += 1
                        elif result == "TIE":
                            ties += 1
                    else:
                        item["score"] = "경기 종료 (상세 스코어 집계 중)"
                        item["result"] = "FINAL"

            except Exception:
                pass

        if next_game is None and schedule_list:
            next_game = schedule_list[0]

        record_str = f"{wins}승 {losses}패" if (wins + losses) > 0 else "2026 시즌 개막 대기 중 (0승 0패)"

        return {
            "season": "2026 NFL Regular Season",
            "team": "Los Angeles Chargers",
            "record": record_str,
            "wins": wins,
            "losses": losses,
            "next_game": next_game,
            "games": schedule_list,
        }

    def _detect_game_result(self, game: Dict[str, any], articles: List[Dict[str, any]]) -> (Optional[str], Optional[str]):
        """Detect final score and win/loss result from collected articles."""
        opp_clean = game["opponent"].lower()
        week_str = f"week {game['week']}"

        for art in articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
            if week_str in text or any(word in text for word in opp_clean.split() if len(word) > 3):
                # Search score pattern like 24-17 or 24 - 17
                scores = re.findall(r"\b(\d{1,2})\s*[-–]\s*(\d{1,2})\b", text)
                if scores:
                    s1, s2 = scores[0]
                    if "win" in text or "defeat" in text or "beat" in text or "over" in text:
                        return f"Chargers {max(int(s1), int(s2))} - {min(int(s1), int(s2))} {game['opponent']}", "WIN"
                    elif "loss" in text or "fall" in text or "fell" in text or "drop" in text:
                        return f"Chargers {min(int(s1), int(s2))} - {max(int(s1), int(s2))} {game['opponent']}", "LOSS"
                    return f"{s1} - {s2}", "FINAL"

        return None, None
