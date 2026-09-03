# ⚡ ChargersPulse 2.0 - LA 차저스 전수 뉴스 수집 및 인텔리전스 리포터

NFL 팀 **로스앤젤레스 차저스(Los Angeles Chargers)** 의 모든 최신 뉴스를 제한 없이 전수 수집하고, 상황에 따른 실시간 트렌드 키워드 자동 추적, 경기/매치업 심층 분석, 중요도 점수 기반 큐레이션 및 주간 정기 자동 실행을 지원하는 인텔리전스 시스템입니다.

---

## ⚡ NewsPulse 2.0 주요 핵심 기능

### 1. 🌐 전수 수집 및 스마트 중요도 선별 (Smart Ranking)
- 20건 제한을 없애고 모든 전문 RSS 피드 및 다중 Google News 쿼리에서 **수집 가능한 모든 뉴스를 전수 수집**.
- **중요도 평가 엔진 (0~100점)**:
  - 🚨 **긴급/핵심 뉴스 (75점 이상)**: 스타터 선수 부상(IR), 53인 최종 로스터 발표, 경기 승패/터치다운, 대형 트레이드
  - ⚡ **주요 뉴스 (55점~74점)**: 인터뷰, 포지션 경쟁, 훈련 캠프 소식
  - 📰 **일반 아카이브**: 전체 수집 뉴스 카테고리별 보관

### 2. 🔥 실시간 상황별 동적 키워드 자동 추적 (Dynamic Keyword Tracker)
- 최신 수집 기사 전체를 실시간 분석하여 **새롭게 부각되는 루키 선수**, **새로운 상대팀**, **긴급 부상 부위** 등을 자동 추출.
- 추출된 트렌드 키워드를 검색 쿼리에 자동 반영하여 상황 변화에 맞춰 수집 풀이 능동적으로 확장됩니다.

### 3. 🏈 경기 및 매치업 전문 분석 센터 (Game & Matchup Center)
- **상대팀 자동 감지**: 샌프란시스코 49ers, 캔자스시티 치프스, 라스베이거스 레이더스 등 매치업 분석.
- **경기 타입 & 스코어 분석**: 프리시즌, 정규시즌 주차, 스코어 현황.
- **공수 핵심 관전 포인트**: 쿼터백(저스틴 허버트) 패싱, 러닝 어택, 수비진 압박 및 세컨더리 분석 전용 섹션 제공.

### 4. ⏰ 일주일 주기 자동 실행 스케줄러 (Weekly Automation)
- **방법 A (파이썬 내장 스케줄러)**: 백그라운드에서 매주 주기적 실행
  ```bash
  python -m newspulse.scheduler --interval-days 7
  ```
- **방법 B (Windows 작업 스케줄러 등록)**: PC에서 매주 정해진 요일/시간에 자동 실행되도록 네이티브 등록
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_weekly_scheduler.ps1 -DayOfWeek Monday -Time 09:00
  ```
- **방법 C (1클릭 배치 실행)**: `scripts\run_weekly.bat` 더블클릭

---

## 🚀 빠른 시작 (Quick Start)

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 전수 수집 및 종합 보고서 생성 (CLI)
```bash
# 전수 수집 및 HTML / Markdown 보고서 동시 생성
python -m newspulse.cli generate --all

# 특정 키워드로 쿼리하고 상위 30건 선별
python -m newspulse.cli generate --query "Justin Herbert" --limit 30

# 등록된 소스 및 동적 확장 쿼리 목록 확인
python -m newspulse.cli sources
```

생성된 보고서는 `./reports/` 폴더에 타임스탬프 파일명 및 `chargers_briefing_latest.html`, `chargers_briefing_latest.md`로 저장됩니다.

---

### 3. Streamlit 인터랙티브 웹 대시보드 실행
```bash
python -m streamlit run newspulse/ui/app.py
```
브라우저(`http://localhost:8501`)에서:
- **전수 수집 모드** 체크 및 원클릭 브리핑 생성
- **🏈 Game Center** 경기/매치업 분석 확인
- **🔥 실시간 트렌드 키워드** 배지 확인
- **🚨 최우선 핵심 뉴스 TOP 3** 및 카테고리별 전체 아카이브 확인
- **HTML / Markdown 보고서 즉시 다운로드**

---

## 📁 프로젝트 구조

```
cool-rutherford/
├── newspulse/
│   ├── __init__.py
│   ├── config.py              # 차저스 RSS, 상대팀 DB, 테마 컬러 설정
│   ├── collector/             # 뉴스 수집기 (RSS, Google News, Scraper)
│   ├── processor/             # 지능형 처리 엔진
│   │   ├── deduplicator.py    # 중복 뉴스 필터링
│   │   ├── categorizer.py     # 카테고리 자동 분류
│   │   ├── ranker.py          # 중요도 점수 산출 및 핵심 선별 (0~100점)
│   │   ├── dynamic_keywords.py# 실시간 트렌드 키워드 자동 추출
│   │   ├── game_analyzer.py   # 경기/매치업 전문 분석
│   │   └── summarizer.py      # 한국어 브리핑 & 요약 엔진
│   ├── reporter/              # 보고서 생성기 (HTML 대시보드, Markdown)
│   ├── ui/                    # Streamlit 웹 대시보드
│   ├── scheduler.py           # 주간 자동 실행 스케줄러
│   └── cli.py                 # CLI 명령어 진입점
├── scripts/
│   ├── run_weekly.bat         # 1클릭 주간 실행 배치 스크립트
│   └── setup_weekly_scheduler.ps1 # Windows 작업 스케줄러 자동 등록
├── reports/                   # 생성된 보고서 저장 디렉토리
├── tests/                     # 단위 테스트 스위트 (10개 테스트)
├── requirements.txt
└── README.md
```

---

## 🧪 테스트 실행

```bash
python -m pytest tests/ -v
```
