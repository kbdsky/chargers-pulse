"""Streamlit Dashboard for LA Chargers Intelligence Center (NewsPulse 2.0)."""

import os
import sys
from pathlib import Path
import streamlit as st

parent_dir = str(Path(__file__).resolve().parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from newspulse.config import CHARGERS_RSS_FEEDS, BASE_GOOGLE_NEWS_QUERIES
from newspulse.collector import RSSCollector, GoogleNewsCollector
from newspulse.processor import (
    Deduplicator,
    Categorizer,
    Summarizer,
    ArticleRanker,
    DynamicKeywordTracker,
    GameAnalyzer,
)
from newspulse.reporter import HTMLReporter, MarkdownReporter

# Page configuration
st.set_page_config(
    page_title="⚡ ChargersPulse 2.0 - LA 차저스 인텔리전스 센터",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Chargers Theme
st.markdown(
    """
    <style>
    .main { background-color: #07101E; color: #F1F5F9; }
    .stApp { background: linear-gradient(180deg, #07101E 0%, #0C1E38 100%); }
    .chargers-hero {
        background: linear-gradient(135deg, #0C2340 0%, #004D7A 50%, #0080C6 100%);
        border-radius: 14px;
        padding: 22px 28px;
        border-bottom: 4px solid #FFC20E;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    .chargers-hero h1 { color: #FFFFFF !important; font-size: 2.1rem; margin-bottom: 4px; font-weight: 800; }
    .chargers-hero p { color: #E2E8F0; font-size: 0.95rem; margin: 0; }
    .briefing-box {
        background: #0C1E38;
        border: 1px solid #1E3E6B;
        border-left: 5px solid #FFC20E;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
    }
    .game-box {
        background: #102A4E;
        border: 1px solid #1E3E6B;
        border-top: 3px solid #0080C6;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
    }
    .article-card {
        background: #132A4D;
        border: 1px solid #1E3E6B;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .badge-cat { background: #0080C6; color: white; padding: 2px 7px; border-radius: 5px; font-size: 0.75rem; font-weight: 600; }
    .badge-tier { background: rgba(255, 194, 14, 0.2); color: #FFC20E; border: 1px solid #FFC20E; padding: 2px 7px; border-radius: 5px; font-size: 0.75rem; font-weight: 700; }
    .badge-source { color: #FFC20E; font-size: 0.78rem; font-weight: 600; }
    .trend-pill { background: #132A4D; border: 1px solid #0080C6; color: #38b6ff; padding: 3px 10px; border-radius: 16px; font-size: 0.8rem; margin-right: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Los_Angeles_Chargers_logo.svg/200px-Los_Angeles_Chargers_logo.svg.png", width=110)
    st.title("⚡ ChargersPulse 2.0")
    st.caption("LA 차저스 전수 수집 및 인텔리전스 센터")
    st.markdown("---")

    st.subheader("⚙️ 수집 모드")
    full_collection = st.checkbox("전수 수집 모드 (제한 없음)", value=True, help="체크 시 모든 RSS 및 구글 뉴스 쿼리를 전수 수집합니다.")
    
    if not full_collection:
        article_limit = st.slider("수집할 최대 기사 수", min_value=10, max_value=80, value=30, step=5)
    else:
        article_limit = None

    st.subheader("📡 RSS 소스")
    selected_feeds = []
    for feed in CHARGERS_RSS_FEEDS:
        if st.checkbox(feed["name"], value=True):
            selected_feeds.append(feed)

    st.subheader("🤖 AI 요약 설정 (선택)")
    gemini_key = st.text_input("Gemini API Key (생략 시 자체 요약)", type="password")

    generate_clicked = st.button("⚡ 전수 수집 및 브리핑 생성", type="primary", use_container_width=True)

# Main Dashboard
st.markdown(
    """
    <div class="chargers-hero">
        <h1>⚡ LA CHARGERS INTELLIGENCE CENTER</h1>
        <p>전수 뉴스 수집, 중요도 점수 평가, 실시간 트렌드 키워드 추적, 경기/매치업 심층 분석</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# State initialization
if "articles" not in st.session_state:
    st.session_state.articles = []
if "briefing" not in st.session_state:
    st.session_state.briefing = None
if "html_report" not in st.session_state:
    st.session_state.html_report = ""
if "md_report" not in st.session_state:
    st.session_state.md_report = ""

# Data Fetching
if generate_clicked or not st.session_state.articles:
    with st.spinner("🌐 차저스 관련 전수 뉴스를 수집하고 트렌드 및 중요도를 분석하는 중입니다..."):
        all_raw = []

        # 1. Fetch RSS
        if selected_feeds:
            rss_collector = RSSCollector()
            rss_items = rss_collector.fetch_multiple_feeds(selected_feeds, limit_per_feed=50)
            all_raw.extend(rss_items)

        # 2. Fetch Google News
        kw_tracker = DynamicKeywordTracker()
        search_queries = kw_tracker.get_search_queries()

        gnews_collector = GoogleNewsCollector()
        gnews_items = gnews_collector.search_queries(search_queries, limit_per_query=20)
        all_raw.extend(gnews_items)

        # 3. Deduplicate
        deduplicator = Deduplicator(similarity_threshold=0.6)
        unique = deduplicator.deduplicate(all_raw)

        # 4. Extract Dynamic Trends
        kw_tracker.extract_trends_from_articles(unique)

        # 5. Categorize & Rank
        categorizer = Categorizer()
        categorized = categorizer.categorize_all(unique)

        ranker = ArticleRanker()
        ranked = ranker.rank_articles(categorized)

        if article_limit is not None:
            ranked = ranked[:article_limit]

        # 6. Summarize & Briefing
        summarizer = Summarizer(api_key=gemini_key if gemini_key else None)
        summarized = summarizer.summarize_all(ranked)
        briefing = summarizer.generate_executive_briefing(summarized)

        # 7. Exporters
        html_reporter = HTMLReporter()
        html_content = html_reporter.render(summarized, briefing)

        md_reporter = MarkdownReporter()
        md_content = md_reporter.render(summarized, briefing)

        st.session_state.articles = summarized
        st.session_state.briefing = briefing
        st.session_state.html_report = html_content
        st.session_state.md_report = md_content

# Display Content
if st.session_state.articles and st.session_state.briefing:
    briefing = st.session_state.briefing
    articles = st.session_state.articles

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("전수 수집 기사", f"{len(articles)}건")
    with m2:
        top_cnt = len([a for a in articles if a.get("importance_score", 0) >= 70])
        st.metric("🚨 긴급/핵심 뉴스", f"{top_cnt}건")
    with m3:
        games_cnt = len([a for a in articles if a.get("category_key") == "game"])
        st.metric("🏈 경기/매치업 보도", f"{games_cnt}건")
    with m4:
        injuries_cnt = len([a for a in articles if a.get("category_key") == "injury"])
        st.metric("📋 부상/로스터 리포트", f"{injuries_cnt}건")

    # Executive Briefing
    st.markdown(
        f"""
        <div class="briefing-box">
            <h3 style="color: #FFC20E; margin-bottom: 10px;">⚡ {briefing.get('headline', '')}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_cols = st.columns(2)
    takeaways = briefing.get("key_takeaways", [])
    for idx, item in enumerate(takeaways):
        col = t_cols[idx % 2]
        col.info(item)

    # Dynamic Trends Pills
    trends = briefing.get("trending_keywords", [])
    if trends:
        trend_html = " ".join([f'<span class="trend-pill">#{kw}</span>' for kw in trends])
        st.markdown(f"**🔥 실시간 트렌드 키워드:** {trend_html}", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

    # Game Intelligence Center
    game_center = briefing.get("game_center", {})
    if game_center and game_center.get("has_game_data"):
        st.markdown(
            f"""
            <div class="game-box">
                <h4 style="color: #FFFFFF; margin-bottom: 8px;">🏈 경기 및 매치업 분석 (Game Center)</h4>
                <div style="display: flex; gap: 10px; margin-bottom: 12px;">
                    <span class="badge-tier">상대: {game_center.get('opponent', '')}</span>
                    <span class="badge-cat">구분: {game_center.get('game_type', '')}</span>
                    <span class="badge-source">스코어/현황: {game_center.get('score_detected', '')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        gc1, gc2 = st.columns(2)
        with gc1:
            st.write(f"⚔️ **공격진(Offense):** {game_center.get('offense_notes', '')}")
        with gc2:
            st.write(f"🛡️ **수비진(Defense):** {game_center.get('defense_notes', '')}")

    st.markdown("---")

    # Download Buttons
    d1, d2, _ = st.columns([1, 1, 2])
    with d1:
        st.download_button(
            label="📥 HTML 보고서 다운로드",
            data=st.session_state.html_report,
            file_name="chargers_intelligence_report.html",
            mime="text/html",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            label="📥 Markdown 보고서 다운로드",
            data=st.session_state.md_report,
            file_name="chargers_intelligence_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Top Highlights Section
    top_highlights = briefing.get("top_highlights", [])
    if top_highlights:
        st.markdown("### 🚨 최우선 핵심 뉴스 (Top Priority Highlights)")
        h_cols = st.columns(min(len(top_highlights), 3))
        for idx, h in enumerate(top_highlights[:3]):
            col = h_cols[idx]
            with col:
                st.markdown(
                    f"""
                    <div class="article-card" style="border-top: 3px solid #FFC20E;">
                        <span class="badge-tier">점수: {h.get('importance_score', 0)}점</span>
                        <span class="badge-cat">{h.get('category_badge', '')}</span>
                        <h4 style="color: #FFFFFF; margin: 8px 0 4px 0;">{h.get('headline_kr', h.get('title'))}</h4>
                        <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 8px;">{h.get('title')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for b in h.get("summary_bullets_kr", []):
                    st.write(f"- {b}")
                st.link_button("원문 보기 ↗", h.get("url", "#"))

    st.markdown("---")
    st.markdown(f"### 📰 전체 수집 뉴스 아카이브 ({len(articles)}건)")

    tabs = st.tabs(["전체 보기", "⚡ 경기 소식", "📋 부상/로스터", "🎯 영입/계약", "🎙️ 인터뷰", "⚡ 팀 소식"])
    cat_keys = ["all", "game", "injury", "roster", "interview", "general"]

    for tab, cat_key in zip(tabs, cat_keys):
        with tab:
            tab_articles = articles if cat_key == "all" else [a for a in articles if a.get("category_key") == cat_key]
            if not tab_articles:
                st.info("해당 카테고리의 뉴스가 없습니다.")
            else:
                for art in tab_articles:
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="article-card">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <div>
                                        <span class="badge-tier">{art.get('priority_tier', '')} ({art.get('importance_score', 0)}점)</span>
                                        <span class="badge-cat">{art.get('category_badge', '')}</span>
                                        <span class="badge-source">📰 {art.get('source', '')}</span>
                                    </div>
                                    <span style="font-size: 0.78rem; color: #94A3B8;">{art.get('published', '')[:10]}</span>
                                </div>
                                <h4 style="color: #FFFFFF; margin: 4px 0;">{art.get('headline_kr', art.get('title'))}</h4>
                                <div style="font-size: 0.82rem; color: #94A3B8; font-style: italic; margin-bottom: 8px;">{art.get('title')}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        for b in art.get("summary_bullets_kr", []):
                            st.write(f"- {b}")
                        st.link_button("원문 기사 읽기 ↗", art.get("url", "#"))
                        st.markdown("<br/>", unsafe_allow_html=True)
