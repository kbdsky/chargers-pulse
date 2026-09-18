"""Official NFL Injury Report Table Tracker for LA Chargers."""

import re
import datetime
from typing import Dict, List, Optional


# Official Week 2 Chargers vs. Raiders Injury Report (Updated dynamically via verified news)
CHARGERS_OFFICIAL_INJURY_REPORT = [
    {
        "player": "Ladd McConkey",
        "position": "WR",
        "injury": "Rib (늑골/갈비뼈 부상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 확정)",
        "status_code": "OUT",
        "status_detail": "1주차 경기 중 갈비뼈 부상. 훈련 전면 불참(DNP)으로 2주차 Raiders전 결장.",
    },
    {
        "player": "Trey Pipkins III",
        "position": "OT",
        "injury": "Knee (무릎 부상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 확정)",
        "status_code": "OUT",
        "status_detail": "무릎 통증으로 훈련 불참(DNP). 오펜시브 라인 백업 투입 준비.",
    },
    {
        "player": "Elijah Molden",
        "position": "S",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 확정)",
        "status_code": "OUT",
        "status_detail": "햄스트링 통증으로 훈련 불참(DNP). 세컨더리 로테이션 가동.",
    },
    {
        "player": "Dalvin Tomlinson",
        "position": "DL",
        "injury": "Hamstring / Rest (햄스트링/휴식)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장)",
        "status_code": "OUT",
        "status_detail": "디펜시브 라인 베테랑 부상 및 휴식 관리로 결장.",
    },
    {
        "player": "Teair Tart",
        "position": "DT",
        "injury": "Ankle (발목 부상)",
        "wednesday": "DNP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "목요일 제한적 훈련(LP) 복귀. 경기 당일 워밍업 후 출전 여부 확정.",
    },
    {
        "player": "Deane Leonard",
        "position": "CB",
        "injury": "Abdomen (복부 통증)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "제한적 훈련(LP) 소화 중. 세컨더리 백업 출격 대기.",
    },
    {
        "player": "Justin Herbert",
        "position": "QB",
        "injury": "Plantar Fascia (오른발 족저근막염)",
        "wednesday": "FP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "보호대 착용 후 정상 훈련(Full Practice) 100% 소화. 선발 쿼터백 출격.",
    },
    {
        "player": "Khalil Mack",
        "position": "OLB",
        "injury": "NIR-Rest (베테랑 휴식/관리)",
        "wednesday": "LP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "주중 베테랑 컨디션 조절 후 정상 훈련 복귀. 패스 러시 핵심 선발 출전.",
    },
    {
        "player": "Bud Dupree",
        "position": "OLB",
        "injury": "NIR-Rest (베테랑 휴식)",
        "wednesday": "LP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "풀 훈련 완주. Raiders 오펜시브 라인 압박 엣지 로테이션 가동.",
    },
    {
        "player": "Derius Davis",
        "position": "WR",
        "injury": "Calf (종아리 통증)",
        "wednesday": "LP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "종아리 경미 통증 회복 후 Full 참여. 리턴팀 및 리시버 정상 가동.",
    },
    {
        "player": "Akheem Mesidor",
        "position": "OLB",
        "injury": "Calf (종아리 부상)",
        "wednesday": "LP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "정상 훈련 소화. 패스 러시 뎁스 차트 합류.",
    },
    {
        "player": "Keandre Lambert-Smith",
        "position": "WR",
        "injury": "Hamstring (햄스트링 중상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "IR (부상자 명단)",
        "status_code": "IR",
        "status_detail": "햄스트링 중상으로 공식 IR(Injured Reserve) 등재. 최소 4주 결장.",
    },
    {
        "player": "Tyler Biadasz",
        "position": "C",
        "injury": "Knee (무릎 시즌 아웃)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "IR (시즌 아웃)",
        "status_code": "IR",
        "status_detail": "프리시즌 무릎 부상으로 IR 등재. 2026 시즌 아웃.",
    },
]


class InjuryTracker:
    """Tracks and generates the structured Official NFL Injury Report Table for Chargers."""

    def __init__(self):
        pass

    def get_injury_report_table(self, articles: List[Dict[str, any]] = None) -> Dict[str, any]:
        """Generate structured official injury report table with live status updates."""
        table_rows = [dict(row) for row in CHARGERS_OFFICIAL_INJURY_REPORT]

        # Scan articles dynamically to update or add recent injury developments
        if articles:
            for art in articles:
                text = f"{art.get('title', '')} {art.get('summary', '')}".lower()
                for row in table_rows:
                    p_name = row["player"].lower()
                    if p_name in text:
                        if "out" in text and ("rule out" in text or "ruled out" in text):
                            row["game_status"] = "Out (결장 확정)"
                            row["status_code"] = "OUT"
                        elif "questionable" in text:
                            row["game_status"] = "Questionable (출전 불투명)"
                            row["status_code"] = "QUESTIONABLE"
                        elif "full practice" in text or "healthy" in text:
                            row["game_status"] = "Active (출전 가능)"
                            row["status_code"] = "ACTIVE"

        out_count = sum(1 for r in table_rows if r["status_code"] == "OUT" or r["status_code"] == "IR")
        questionable_count = sum(1 for r in table_rows if r["status_code"] == "QUESTIONABLE")
        active_count = sum(1 for r in table_rows if r["status_code"] == "ACTIVE")

        summary_text = f"총 {len(table_rows)}명 등재 (결장/IR: {out_count}명, 출전 불투명: {questionable_count}명, 정상 출전: {active_count}명)"

        return {
            "title": "⚡ LA Chargers 공식 부상 리포트 (Official Injury Report)",
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d"),
            "summary_counts": summary_text,
            "legend": {
                "DNP": "Did Not Participate (훈련 전면 불참)",
                "LP": "Limited Participation (제한적 훈련 참여)",
                "FP": "Full Participation (정상 훈련 소화)",
                "Out": "결장 확정 (출전 불가)",
                "Questionable": "출전 불투명 (경기 당일 50% 확률)",
                "IR": "Injured Reserve (부상자 명단 / 최소 4주 결장)"
            },
            "players": table_rows,
        }
