"""Configuration for NewsPulse 2.0 (LA Chargers Edition)."""

from typing import Dict, List
import os

# Primary Curated RSS Feeds
CHARGERS_RSS_FEEDS = [
    {
        "name": "Bolts From The Blue (SB Nation)",
        "url": "https://www.boltsfromtheblue.com/rss/index.xml",
        "category": "전문 팬 매체/블로그",
        "filter_chargers": False,
        "weight": 1.0,
    },
    {
        "name": "Yardbarker (LA Chargers Feed)",
        "url": "https://www.yardbarker.com/rss/team/41",
        "category": "전문 스포츠 미디어",
        "filter_chargers": True,
        "weight": 1.0,
    },
    {
        "name": "ESPN NFL News",
        "url": "https://www.espn.com/espn/rss/nfl/news",
        "category": "종합 스포츠",
        "filter_chargers": True,
        "weight": 0.9,
    },
    {
        "name": "Reddit r/Chargers",
        "url": "https://www.reddit.com/r/Chargers/hot/.rss",
        "category": "커뮤니티",
        "filter_chargers": False,
        "weight": 0.7,
    },
]

# Baseline Google News Search Queries (Expanded dynamically)
BASE_GOOGLE_NEWS_QUERIES = [
    "Los Angeles Chargers",
    "LA Chargers",
    "Justin Herbert Chargers",
    "Jim Harbaugh Chargers",
    "Chargers injury roster",
    "Chargers preseason game recap",
]

# NFL Teams / Opponents for Matchup Detection
NFL_TEAMS = {
    "49ers": "샌프란시스코 포티나이너스 (SF 49ers)",
    "chiefs": "캔자스시티 치프스 (KC Chiefs)",
    "raiders": "라스베이거스 레이더스 (LV Raiders)",
    "broncos": "덴버 브롱코스 (DEN Broncos)",
    "rams": "LA 램스 (LA Rams)",
    "cowboys": "댈러스 카우보이스 (DAL Cowboys)",
    "eagles": "필라델피아 이글스 (PHI Eagles)",
    "packers": "그린베이 패커스 (GB Packers)",
    "lions": "디트로이트 라이온스 (DET Lions)",
    "ravens": "볼티모어 레이븐스 (BAL Ravens)",
    "bills": "버팔로 빌스 (BUF Bills)",
    "bengals": "신시내티 벵골스 (CIN Bengals)",
    "dolphins": "마이애미 돌핀스 (MIA Dolphins)",
    "patriots": "뉴잉글랜드 패트리어츠 (NE Patriots)",
    "jets": "뉴욕 제츠 (NY Jets)",
    "steelers": "피츠버그 스틸러스 (PIT Steelers)",
    "browns": "클리블랜드 브라운스 (CLE Browns)",
    "texans": "휴스턴 텍산스 (HOU Texans)",
    "colts": "인디애나폴리스 콜츠 (IND Colts)",
    "jaguars": "잭슨빌 재규어스 (JAX Jaguars)",
    "titans": "테네시 타이탄스 (TEN Titans)",
    "seahawks": "시애틀 시호크스 (SEA Seahawks)",
    "cardinals": "애리조나 카디널스 (ARI Cardinals)",
    "saints": "뉴올리언스 세인츠 (NO Saints)",
    "buccaneers": "탬파베이 버커니어스 (TB Buccaneers)",
    "falcons": "애틀랜타 팰컨스 (ATL Falcons)",
    "panthers": "캐롤라이나 팬서스 (CAR Panthers)",
    "vikings": "미네소타 바이킹스 (MIN Vikings)",
    "bears": "시카고 베어스 (CHI Bears)",
    "commanders": "워싱턴 커맨더스 (WAS Commanders)",
    "giants": "뉴욕 자이언츠 (NY Giants)",
}

# Dynamic keyword cache path
DYNAMIC_KEYWORD_FILE = os.path.join(os.path.dirname(__file__), "dynamic_keywords.json")

# Category Classification Rules
CATEGORY_RULES: Dict[str, Dict[str, any]] = {
    "game": {
        "name": "경기 결과/프리뷰",
        "badge": "⚡ 경기 소식",
        "icon": "🏈",
        "keywords": [
            "vs", "game", "score", "highlights", "win", "loss", "recap", "preview",
            "touchdown", "quarter", "playoff", "preseason", "week", "joint practice",
            "final", "scrimmage", "경기", "승리", "패배", "터치다운", "합동 훈련"
        ],
    },
    "injury": {
        "name": "부상/로스터 보고",
        "badge": "📋 부상/로스터",
        "icon": "🏥",
        "keywords": [
            "injury", "injured", "ir", "ankle", "knee", "hamstring", "concussion",
            "questionable", "doubtful", "out", "pup", "surgery", "hurt", "limping",
            "부상", "결장", "수술", "이탈", "뇌진탕", "재활"
        ],
    },
    "roster": {
        "name": "계약/트레이드/드래프트",
        "badge": "🎯 영입/계약",
        "icon": "✍️",
        "keywords": [
            "sign", "signed", "signing", "waive", "waived", "release", "released",
            "contract", "extension", "trade", "traded", "draft", "roster", "practice squad",
            "53-man", "cut", "free agent", "계약", "영입", "방출", "트레이드", "드래프트", "연장"
        ],
    },
    "interview": {
        "name": "감독/선수 인터뷰",
        "badge": "🎙️ 인터뷰/발언",
        "icon": "🎙️",
        "keywords": [
            "harbaugh", "herbert", "coach", "press conference", "says", "quote",
            "discusses", "interview", "speaks", "thoughts", "addresses", "comments",
            "하보", "허버트", "인터뷰", "기자회견", "감독", "발언"
        ],
    },
    "general": {
        "name": "팀 일반 소식",
        "badge": "⚡ 팀 소식",
        "icon": "⚡",
        "keywords": [],
    },
}

# Theme Colors (LA Chargers Official Palette)
THEME_COLORS = {
    "powder_blue": "#0080C6",
    "sunshine_gold": "#FFC20E",
    "navy": "#0C2340",
    "white": "#FFFFFF",
    "bg_dark": "#07101E",
    "card_dark": "#0C1E38",
    "card_inner": "#132A4D",
}
