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
        "status": "final",
        "score": "Chargers 14 - 26 Arizona Cardinals (AZ Cardinals)",
        "result": "LOSS",
    },
    {
        "week": 2,
        "date_utc": "2026-09-20T20:05:00Z",
        "date_kst": "2026년 9월 21일 (월) 오전 05:05 (KST)",
        "opponent": "Las Vegas Raiders (LV Raiders)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 2주차 (지구 홈경기)",
        "status": "final",
        "score": "Chargers 14 - 26 Las Vegas Raiders (LV Raiders)",
        "result": "LOSS",
    },
    {
        "week": 3,
        "date_utc": "2026-09-27T17:00:00Z",
        "date_kst": "2026년 9월 28일 (월) 오전 02:00 (KST)",
        "opponent": "Buffalo Bills (BUF Bills)",
        "is_home": False,
        "stadium": "Highmark Stadium (Orchard Park, NY)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 3주차 (버팔로 원정)",
        "status": "final",
        "score": "Chargers 16 - 24 Buffalo Bills (BUF Bills)",
        "result": "LOSS",
    },
    {
        "week": 4,
        "date_utc": "2026-10-04T20:25:00Z",
        "date_kst": "2026년 10월 5일 (월) 오전 05:25 (KST)",
        "opponent": "Seattle Seahawks (SEA Seahawks)",
        "is_home": False,
        "stadium": "Lumen Field (Seattle, WA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 4주차 (시애틀 원정)",
        "status": "final",
        "score": "Chargers 23 - 30 Seattle Seahawks (SEA Seahawks)",
        "result": "LOSS",
    },
    {
        "week": 5,
        "date_utc": "2026-10-11T20:05:00Z",
        "date_kst": "2026년 10월 12일 (월) 오전 05:05 (KST)",
        "opponent": "Denver Broncos (DEN Broncos)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 5주차 (지구 홈경기)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 6,
        "date_utc": "2026-10-18T20:25:00Z",
        "date_kst": "2026년 10월 19일 (월) 오전 05:25 (KST)",
        "opponent": "Kansas City Chiefs (KC Chiefs)",
        "is_home": False,
        "stadium": "GEHA Field at Arrowhead (Kansas City, MO)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 6주차 (치프스 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 7,
        "date_utc": None,
        "date_kst": "2026년 10월 26일 주간",
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
        "week": 8,
        "date_utc": "2026-11-01T21:05:00Z",
        "date_kst": "2026년 11월 2일 (월) 오전 06:05 (KST)",
        "opponent": "Los Angeles Rams (LA Rams)",
        "is_home": False,
        "stadium": "SoFi Stadium (Inglewood, CA - Rams 홈)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 8주차 (LA 더비 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 9,
        "date_utc": "2026-11-08T21:05:00Z",
        "date_kst": "2026년 11월 9일 (월) 오전 06:05 (KST)",
        "opponent": "Houston Texans (HOU Texans)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "CBS (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 9주차 홈경기",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 10,
        "date_utc": "2026-11-17T01:15:00Z",
        "date_kst": "2026년 11월 17일 (화) 오전 10:15 (KST)",
        "opponent": "Baltimore Ravens (BAL Ravens)",
        "is_home": False,
        "stadium": "M&T Bank Stadium (Baltimore, MD)",
        "broadcast": "ESPN/ABC (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 10주차 (먼데이 나이트 풋볼)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 11,
        "date_utc": "2026-11-22T21:05:00Z",
        "date_kst": "2026년 11월 23일 (월) 오전 06:05 (KST)",
        "opponent": "New York Jets (NY Jets)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "FOX (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 11주차 홈경기",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 12,
        "date_utc": "2026-11-30T01:20:00Z",
        "date_kst": "2026년 11월 30일 (월) 오전 10:20 (KST)",
        "opponent": "New England Patriots (NE Patriots)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "NBC (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 12주차 (선데이 나이트 풋볼)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 13,
        "date_utc": "2026-12-06T18:00:00Z",
        "date_kst": "2026년 12월 6일 (일, 현지) · 킥오프 시간 미정 (NFL 발표 대기)",
        "opponent": "Tampa Bay Buccaneers (TB Buccaneers)",
        "is_home": False,
        "stadium": "Raymond James Stadium (Tampa, FL)",
        "broadcast": "중계사 미정 | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 13주차 (탬파베이 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 14,
        "date_utc": "2026-12-13T21:05:00Z",
        "date_kst": "2026년 12월 13일 (일, 현지) · 킥오프 시간 미정 (NFL 발표 대기)",
        "opponent": "Las Vegas Raiders (LV Raiders)",
        "is_home": False,
        "stadium": "Allegiant Stadium (Las Vegas, NV)",
        "broadcast": "중계사 미정 | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 14주차 (라스베이거스 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 15,
        "date_utc": "2026-12-18T01:15:00Z",
        "date_kst": "2026년 12월 18일 (금) 오전 10:15 (KST)",
        "opponent": "San Francisco 49ers (SF 49ers)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "Prime Video (미국) | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 15주차 (서스데이 나이트 풋볼)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 16,
        "date_utc": "2026-12-27T18:00:00Z",
        "date_kst": "2026년 12월 26~27일 주간 (현지) · 요일/킥오프 시간 미정 (플렉스 스케줄)",
        "opponent": "Miami Dolphins (MIA Dolphins)",
        "is_home": False,
        "stadium": "Hard Rock Stadium (Miami Gardens, FL)",
        "broadcast": "중계사 미정 | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 16주차 (마이애미 원정)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 17,
        "date_utc": "2027-01-03T21:25:00Z",
        "date_kst": "2027년 1월 2~3일 주간 (현지) · 요일/킥오프 시간 미정 (15주차 종료 후 발표)",
        "opponent": "Kansas City Chiefs (KC Chiefs)",
        "is_home": True,
        "stadium": "SoFi Stadium (Los Angeles, CA)",
        "broadcast": "중계사 미정 | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 17주차 (치프스 홈경기)",
        "status": "upcoming",
        "score": None,
        "result": None,
    },
    {
        "week": 18,
        "date_utc": "2027-01-10T21:25:00Z",
        "date_kst": "2027년 1월 9~10일 주간 (현지) · 요일/킥오프 시간 미정 (17주차 종료 후 발표)",
        "opponent": "Denver Broncos (DEN Broncos)",
        "is_home": False,
        "stadium": "Empower Field at Mile High (Denver, CO)",
        "broadcast": "중계사 미정 | DAZN(한국 전경기) / 쿠팡플레이(선별)",
        "game_type": "정규시즌 18주차 최종전 (덴버 원정)",
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
                    elif item.get("score") and item.get("result"):
                        pass
                    else:
                        item["score"] = "경기 종료 (상세 스코어 집계 중)"
                        item["result"] = "FINAL"

                    res = item.get("result")
                    if res == "WIN":
                        wins += 1
                    elif res == "LOSS":
                        losses += 1
                    elif res == "TIE":
                        ties += 1

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
        """Detect final score and win/loss result from collected articles with strict accuracy."""
        opp_clean = game["opponent"].lower()
        week_num = game["week"]
        week_str = f"week {week_num}"

        for art in articles:
            text = f"{art.get('title', '')} {art.get('summary', '')}".lower()

            # Check if this article discusses this specific week or opponent
            has_opp = any(word in text for word in opp_clean.split() if len(word) > 3)
            has_week = week_str in text or (week_num == 1 and ("season opener" in text or "opener" in text))
            if not (has_opp and has_week):
                continue

            # Search score pattern like 26-14 or 26 - 14
            scores = re.findall(r"\b(\d{1,2})\s*[-–]\s*(\d{1,2})\b", text)
            if scores:
                s1, s2 = int(scores[0][0]), int(scores[0][1])
                higher_score = max(s1, s2)
                lower_score = min(s1, s2)

                # Prioritize loss indicators to prevent false positive from "must-win"
                is_loss = (
                    "loss" in text
                    or "lost" in text
                    or "upset by" in text
                    or "upset loss" in text
                    or "stun chargers" in text
                    or "stuns chargers" in text
                    or "fell to" in text
                    or "fall to" in text
                    or "defeated by" in text
                    or "wrong end" in text
                    or "lose their" in text
                )
                is_win = (
                    ("chargers win" in text or "chargers defeat" in text or "win over" in text or "victory over" in text or "chargers beat" in text)
                    and not ("must-win" in text or "need a win" in text or "loss" in text or "lost" in text)
                )

                if is_loss:
                    return f"Chargers {lower_score} - {higher_score} {game['opponent']}", "LOSS"
                elif is_win:
                    return f"Chargers {higher_score} - {lower_score} {game['opponent']}", "WIN"
                else:
                    if "loss" in text or "lost" in text or "lose" in text:
                        return f"Chargers {lower_score} - {higher_score} {game['opponent']}", "LOSS"
                    return f"Chargers {s1} - {s2} {game['opponent']}", "FINAL"

        return None, None
