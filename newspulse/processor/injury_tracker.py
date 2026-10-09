"""Official NFL Injury Report Table Tracker for LA Chargers."""

import re
import datetime
from typing import Dict, List, Optional


# Official Week 5 Chargers vs. Broncos Injury Report
# Basis: Chargers official practice reports — Wed 2026-10-07, Thu 2026-10-08.
# The Friday (2026-10-09) final report with game designations (Out/Doubtful/Questionable)
# has NOT been released yet, so "friday" stays "-" and undecided players use status_code "PENDING".
# Never fill friday/game designations with guesses — update only from the official report.
REPORT_WEEK_LABEL = "5주차 vs Denver Broncos"
REPORT_BASIS = "2026-10-08 (목) 공식 연습 리포트 기준"
FRIDAY_REPORT_DATE = datetime.date(2026, 10, 9)
PENDING_STATUS = "미정 (금요일 최종 리포트 대기)"

CHARGERS_OFFICIAL_INJURY_REPORT = [
    # --- Did Not Practice (Thursday) ---
    {
        "player": "Joe Alt",
        "position": "OT",
        "injury": "Neck (목)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 연속 훈련 불참(DNP). 출전 여부는 금요일 리포트에서 확정.",
    },
    {
        "player": "Rashawn Slater",
        "position": "OT",
        "injury": "Ankle (발목)",
        "wednesday": "-",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "4주차 Seahawks전에서 하이 앵클 스프레인. 목요일 DNP, 현지 언론에서 IR 등재 가능성 거론.",
    },
    {
        "player": "Trevor Penning",
        "position": "OL",
        "injury": "Concussion (뇌진탕)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "뇌진탕 프로토콜 진행 중. 수·목 연속 DNP.",
    },
    {
        "player": "Kayode Awosika",
        "position": "G",
        "injury": "Fibula (비골)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "비골 부상으로 수·목 연속 DNP.",
    },
    {
        "player": "Donte Jackson",
        "position": "CB",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "햄스트링 부상으로 수·목 연속 DNP.",
    },
    {
        "player": "Derwin James Jr.",
        "position": "S",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "햄스트링 부상으로 수·목 연속 DNP.",
    },
    {
        "player": "Ladd McConkey",
        "position": "WR",
        "injury": "Foot (발)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "발 부상으로 수·목 연속 DNP.",
    },
    {
        "player": "Brenen Thompson",
        "position": "WR",
        "injury": "Quadriceps (대퇴사두근)",
        "wednesday": "LP",
        "thursday": "DNP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수요일 제한적 참여(LP) 후 목요일 불참(DNP)으로 하향.",
    },
    # --- Limited Participation (Wed & Thu) ---
    {
        "player": "Cam Hart",
        "position": "CB",
        "injury": "Knee (무릎)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Alec Ingold",
        "position": "FB",
        "injury": "Shoulder (어깨)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Quentin Johnston",
        "position": "WR",
        "injury": "Chest (흉부)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Charlie Kolar",
        "position": "TE",
        "injury": "Forearm (전완부)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Trey Lance",
        "position": "QB",
        "injury": "Groin (사타구니)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP). 백업 QB.",
    },
    {
        "player": "Deane Leonard",
        "position": "DB",
        "injury": "Rib (갈비뼈)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Scott Matlock",
        "position": "DL/FB",
        "injury": "Foot (발)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Branson Taylor",
        "position": "OL",
        "injury": "Shoulder/Neck (어깨/목)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    {
        "player": "Dalvin Tomlinson",
        "position": "DL",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "-",
        "game_status": PENDING_STATUS,
        "status_code": "PENDING",
        "status_detail": "수·목 제한적 참여(LP).",
    },
    # --- Non-injury rest ---
    {
        "player": "Khalil Mack",
        "position": "OLB",
        "injury": "NIR-Rest (부상 아님, 베테랑 휴식)",
        "wednesday": "DNP",
        "thursday": "FP",
        "friday": "-",
        "game_status": "부상 아님 (목요일 정상 훈련)",
        "status_code": "ACTIVE",
        "status_detail": "수요일 베테랑 휴식(DNP) 후 목요일 정상 훈련(FP).",
    },
    # --- Injured Reserve ---
    {
        "player": "Keandre Lambert-Smith",
        "position": "WR",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "-",
        "thursday": "-",
        "friday": "-",
        "game_status": "IR (부상자 명단)",
        "status_code": "IR",
        "status_detail": "1주차 Cardinals전 부상, 9월 15일 IR 등재. 6주차(10/18 Chiefs전)부터 복귀 가능.",
    },
    {
        "player": "Tyler Biadasz",
        "position": "C",
        "injury": "Knee (무릎, ACL)",
        "wednesday": "-",
        "thursday": "-",
        "friday": "-",
        "game_status": "IR (시즌 아웃)",
        "status_code": "IR",
        "status_detail": "8월 18일 49ers 합동훈련 중 왼쪽 무릎 부상, 시즌 아웃 IR.",
    },
]

# Official-designation phrases only. Loose words like "healthy" or a bare "out" are ignored
# because they produce false status changes.
_RULED_OUT_PATTERNS = ("ruled out", "rules out", "will not play", "won't play")
_DOUBTFUL_PATTERNS = ("listed as doubtful", "is doubtful", "designated doubtful")
_QUESTIONABLE_PATTERNS = ("listed as questionable", "is questionable", "designated questionable")


def _published_date(article: Dict[str, any]) -> Optional[datetime.date]:
    raw = article.get("published") or ""
    try:
        return datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00")).date()
    except ValueError:
        return None


class InjuryTracker:
    """Tracks and generates the structured Official NFL Injury Report Table for Chargers."""

    def __init__(self):
        pass

    def get_injury_report_table(self, articles: List[Dict[str, any]] = None) -> Dict[str, any]:
        """Generate structured official injury report table with live status updates."""
        table_rows = [dict(row) for row in CHARGERS_OFFICIAL_INJURY_REPORT]

        # Apply game designations only from articles published on/after the Friday report date,
        # so last week's "ruled out" stories cannot leak into this week's table.
        if articles:
            for art in articles:
                pub = _published_date(art)
                if pub is None or pub < FRIDAY_REPORT_DATE:
                    continue
                text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
                for row in table_rows:
                    if row["status_code"] == "IR":
                        continue
                    if row["player"].lower() not in text:
                        continue
                    if any(p in text for p in _RULED_OUT_PATTERNS):
                        row["game_status"] = "Out (결장 확정)"
                        row["status_code"] = "OUT"
                    elif any(p in text for p in _DOUBTFUL_PATTERNS):
                        row["game_status"] = "Doubtful (출전 가능성 낮음)"
                        row["status_code"] = "QUESTIONABLE"
                    elif any(p in text for p in _QUESTIONABLE_PATTERNS):
                        row["game_status"] = "Questionable (출전 불투명)"
                        row["status_code"] = "QUESTIONABLE"

        out_count = sum(1 for r in table_rows if r["status_code"] in ("OUT", "IR"))
        questionable_count = sum(1 for r in table_rows if r["status_code"] == "QUESTIONABLE")
        pending_count = sum(1 for r in table_rows if r["status_code"] == "PENDING")
        active_count = sum(1 for r in table_rows if r["status_code"] == "ACTIVE")

        summary_text = (
            f"{REPORT_WEEK_LABEL} · {REPORT_BASIS} · 총 {len(table_rows)}명 "
            f"(결장/IR: {out_count}명, 출전 불투명: {questionable_count}명, "
            f"출전 여부 미정: {pending_count}명, 부상 아님: {active_count}명). "
            f"금요일 최종 리포트 발표 후 Out/Questionable 지정이 확정됩니다."
        )

        return {
            "title": "⚡ LA Chargers 공식 부상 리포트 (Official Injury Report)",
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),
            "report_basis": REPORT_BASIS,
            "summary_counts": summary_text,
            "legend": {
                "DNP": "Did Not Participate (훈련 전면 불참)",
                "LP": "Limited Participation (제한적 훈련 참여)",
                "FP": "Full Participation (정상 훈련 소화)",
                "-": "미발표 또는 해당 일자 리포트 미기재",
                "미정": "금요일 최종 리포트 전 (출전 지정 미발표)",
                "Out": "결장 확정 (출전 불가)",
                "Questionable": "출전 불투명",
                "IR": "Injured Reserve (부상자 명단 / 최소 4경기 결장)"
            },
            "players": table_rows,
        }
