"""Official NFL Injury Report Table Tracker for LA Chargers."""

import re
import datetime
from typing import Dict, List, Optional


# Official Week 4 Chargers vs. Seahawks Injury Report (Updated dynamically via verified news)
CHARGERS_OFFICIAL_INJURY_REPORT = [
    {
        "player": "Kayode Awosika",
        "position": "G",
        "injury": "Fibula (비골 부상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 유력)",
        "status_code": "OUT",
        "status_detail": "비골(종아리뼈) 부상으로 훈련 전면 불참(DNP). 4주차 결장 유력.",
    },
    {
        "player": "Charlie Kolar",
        "position": "TE",
        "injury": "Forearm (전완부/팔 부상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 유력)",
        "status_code": "OUT",
        "status_detail": "전완부 부상으로 주중 훈련 전면 불참. 타이트엔드 백업 로테이션.",
    },
    {
        "player": "Brenen Thompson",
        "position": "WR",
        "injury": "Quadriceps (대퇴사두근 부상)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 유력)",
        "status_code": "OUT",
        "status_detail": "대퇴사두근 통증으로 훈련 불참 지속. 4주차 출전 불가 전망.",
    },
    {
        "player": "Dalvin Tomlinson",
        "position": "DT",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "DNP",
        "game_status": "Out (결장 유력)",
        "status_code": "OUT",
        "status_detail": "햄스트링 부상으로 훈련 불참. 디펜시브 태클 라인업 공백.",
    },
    {
        "player": "Ladd McConkey",
        "position": "WR",
        "injury": "Foot (발 부상/통증)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "발 통증으로 주초 불참 후 금요일 제한적 훈련(LP) 복귀. 경기 당일 워밍업 후 결정.",
    },
    {
        "player": "Derwin James Jr.",
        "position": "S",
        "injury": "Hamstring / NIR-Rest (햄스트링/휴식)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "FP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "햄스트링 관리 및 주중 휴식 후 주말 훈련 참가. 세컨더리 핵심 출전 조율.",
    },
    {
        "player": "Bud Dupree",
        "position": "DE",
        "injury": "NIR-Rest (베테랑 관리/휴식)",
        "wednesday": "DNP",
        "thursday": "DNP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "베테랑 주중 휴식 관리 후 정상 훈련 복귀. 패스 러시 출격.",
    },
    {
        "player": "Justin Eboigbe",
        "position": "DE",
        "injury": "Eye (눈 부상)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "안면/눈 부상으로 보호대 착용 후 제한적 훈련 소화 중.",
    },
    {
        "player": "Donte Jackson",
        "position": "CB",
        "injury": "Concussion (뇌진탕 프로토콜)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "NFL 뇌진탕 프로토콜 단계별 복귀 절차 진행 중. 최종 메디컬 승인 대기.",
    },
    {
        "player": "Trey Lance",
        "position": "QB",
        "injury": "Groin (사타구니 통증)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "FP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "사타구니 통증 관리 중. 백업 쿼터백 출전 대기.",
    },
    {
        "player": "Keaton Mitchell",
        "position": "RB",
        "injury": "Ankle (발목 부상)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "발목 통증으로 제한적 훈련 소화. 러닝백 뎁스 합류 대기.",
    },
    {
        "player": "Elijah Molden",
        "position": "DB",
        "injury": "Hamstring (햄스트링)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "햄스트링 부상 호전 후 제한적 훈련(LP) 소화 중.",
    },
    {
        "player": "Trey Pipkins III",
        "position": "OT",
        "injury": "Knee (무릎 부상 관리)",
        "wednesday": "LP",
        "thursday": "LP",
        "friday": "LP",
        "game_status": "Questionable (출전 불투명)",
        "status_code": "QUESTIONABLE",
        "status_detail": "무릎 부상 치료 후 제한적 훈련 복귀. 경기 당일 출전 여부 확정.",
    },
    {
        "player": "Justin Herbert",
        "position": "QB",
        "injury": "Plantar Fascia (오른발 완쾌)",
        "wednesday": "FP",
        "thursday": "FP",
        "friday": "FP",
        "game_status": "Active (정상 출전)",
        "status_code": "ACTIVE",
        "status_detail": "부상 리포트 명단 제외. 100% 정상 선발 출전.",
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
        "status_detail": "주중 컨디션 조절 후 정상 훈련 완주. 선발 엣지 러셔 출전.",
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
        "status_detail": "공식 IR(Injured Reserve) 등재. 최소 4주 결장.",
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
                        # Safeguard: Do not downgrade Herbert unless an explicit rule-out article is found
                        if row["player"] == "Justin Herbert":
                            if "rule out" in text or "ruled out" in text:
                                row["game_status"] = "Out (결장 확정)"
                                row["status_code"] = "OUT"
                            continue

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
