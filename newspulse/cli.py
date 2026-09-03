"""Command-line interface (CLI) for NewsPulse 2.0 - LA Chargers Intelligence Reporter."""

import argparse
import sys
import os
import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from .config import CHARGERS_RSS_FEEDS, BASE_GOOGLE_NEWS_QUERIES
from .collector import RSSCollector, GoogleNewsCollector
from .processor import (
    Deduplicator,
    Categorizer,
    Summarizer,
    ArticleRanker,
    DynamicKeywordTracker,
    GameAnalyzer,
)
from .reporter import HTMLReporter, MarkdownReporter


def main():
    parser = argparse.ArgumentParser(
        description="⚡ NewsPulse 2.0 - NFL LA Chargers Full Collection & Intelligence Generator",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Collect news and generate reports")
    gen_parser.add_argument(
        "--all", "-a",
        action="store_true",
        default=True,
        help="Full unconstrained collection mode (collect all available news)"
    )
    gen_parser.add_argument(
        "--limit", "-n",
        type=int,
        default=None,
        help="Optional maximum article limit (leave empty for full collection)"
    )
    gen_parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Custom search query (overrides baseline queries)"
    )
    gen_parser.add_argument(
        "--format", "-f",
        choices=["html", "md", "all"],
        default="all",
        help="Output report format: 'html', 'md', or 'all' (default: all)"
    )
    gen_parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="./reports",
        help="Directory to save generated reports (default: ./reports)"
    )
    gen_parser.add_argument(
        "--title",
        type=str,
        default="⚡ LA Chargers 종합 뉴스 인텔리전스 주간 리포트",
        help="Custom title for the report"
    )

    # Command: sources
    subparsers.add_parser("sources", help="List configured news sources and RSS feeds")

    # Command: schedule
    sched_parser = subparsers.add_parser("schedule", help="Start background periodic scheduler")
    sched_parser.add_argument(
        "--days", "-d",
        type=int,
        default=7,
        help="Periodic interval in days (default: 7 for weekly)"
    )

    args = parser.parse_args()

    if not args.command or args.command == "generate":
        run_generate(args if args.command else None)
    elif args.command == "sources":
        print("\n⚡ [NewsPulse] Configured LA Chargers News Sources:", flush=True)
        print("-" * 60, flush=True)
        for i, feed in enumerate(CHARGERS_RSS_FEEDS, 1):
            print(f"{i}. {feed['name']} ({feed['category']})", flush=True)
            print(f"   URL: {feed['url']}", flush=True)
        print("\n🔍 Google News Search Queries (Base + Dynamic):", flush=True)
        kw_tracker = DynamicKeywordTracker()
        queries = kw_tracker.get_search_queries()
        for q in queries:
            print(f"   - {q}", flush=True)
        print("-" * 60, flush=True)
    elif args.command == "schedule":
        from .scheduler import start_scheduler
        start_scheduler(interval_days=args.days)


def run_generate(args=None):
    custom_query = getattr(args, "query", None) if args else None
    limit = getattr(args, "limit", None) if args else None
    fmt = getattr(args, "format", "all") if args else "all"
    output_dir = getattr(args, "output_dir", "./reports") if args else "./reports"
    title = getattr(args, "title", "⚡ LA Chargers 종합 뉴스 인텔리전스 주간 리포트") if args else "⚡ LA Chargers 종합 뉴스 인텔리전스 주간 리포트"

    print("\n" + "=" * 65, flush=True)
    print("⚡ NewsPulse 2.0 - LA Chargers 전수 수집 및 종합 인텔리전스 리포터", flush=True)
    print("=" * 65, flush=True)
    print(f"🏈 대상: Los Angeles Chargers (NFL)", flush=True)
    print(f"📁 출력 폴더: {output_dir}", flush=True)
    print(f"📊 수집 모드: {'전수 수집 (Full Collection)' if limit is None else f'상위 {limit}건 제한'}", flush=True)
    print("-" * 65, flush=True)

    # 1. Collect
    print("[1/5] 🌐 뉴스 데이터 전수 수집 중...", flush=True)
    raw_articles = []

    rss_collector = RSSCollector()
    rss_articles = rss_collector.fetch_multiple_feeds(CHARGERS_RSS_FEEDS, limit_per_feed=50)
    print(f"  ✓ 전용 RSS 피드에서 {len(rss_articles)}개 기사 수집 완료", flush=True)
    raw_articles.extend(rss_articles)

    kw_tracker = DynamicKeywordTracker()
    search_queries = [custom_query] if custom_query else kw_tracker.get_search_queries()
    
    gnews_collector = GoogleNewsCollector()
    gnews_articles = gnews_collector.search_queries(search_queries, limit_per_query=20)
    print(f"  ✓ Google News ({len(search_queries)}개 검색 쿼리)에서 {len(gnews_articles)}개 기사 수집 완료", flush=True)
    raw_articles.extend(gnews_articles)

    if not raw_articles:
        print("⚠️ 수집된 뉴스가 없습니다. 네트워크 연결을 확인하세요.", flush=True)
        return

    # 2. Deduplicate
    print(f"\n[2/5] 🧹 중복 제거 및 데이터 정제 중 (총 {len(raw_articles)}개 수집)...", flush=True)
    deduplicator = Deduplicator(similarity_threshold=0.6)
    unique_articles = deduplicator.deduplicate(raw_articles)
    print(f"  ✓ 중복 필터링 완료: 고유 기사 {len(unique_articles)}개 선별", flush=True)

    # 3. Dynamic Keyword Discovery
    print("\n[3/5] 🔥 실시간 트렌드 및 동적 키워드 추출/업데이트 중...", flush=True)
    trend_state = kw_tracker.extract_trends_from_articles(unique_articles)
    hot_keywords = trend_state.get("trending_keywords", [])
    print(f"  ✓ 감지된 트렌드 키워드: {', '.join(hot_keywords[:6]) if hot_keywords else 'None'}", flush=True)

    # 4. Categorize, Rank, Summarize & Game Analyze
    print("\n[4/5] 🤖 중요도 평가(0~100점) 및 한국어 심층 브리핑 요약 중...", flush=True)
    categorizer = Categorizer()
    categorized_articles = categorizer.categorize_all(unique_articles)

    ranker = ArticleRanker()
    ranked_articles = ranker.rank_articles(categorized_articles)

    if limit is not None:
        ranked_articles = ranked_articles[:limit]

    summarizer = Summarizer()
    summarized_articles = summarizer.summarize_all(ranked_articles)
    briefing = summarizer.generate_executive_briefing(summarized_articles)

    top_critical = [a for a in summarized_articles if a.get("importance_score", 0) >= 70]
    print(f"  ✓ 최우선 핵심 뉴스: {len(top_critical)}건 식별", flush=True)
    print(f"  ✓ 총괄 헤드라인: {briefing.get('headline', '')}", flush=True)

    # 5. Generate Reports
    print("\n[5/5] 📄 차저스 테마 종합 브리핑 보고서 생성 중...", flush=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    if fmt in ["html", "all"]:
        html_path = os.path.join(output_dir, f"chargers_weekly_briefing_{timestamp}.html")
        html_reporter = HTMLReporter()
        html_reporter.save(html_path, summarized_articles, briefing, title=title)
        latest_html = os.path.join(output_dir, "chargers_briefing_latest.html")
        html_reporter.save(latest_html, summarized_articles, briefing, title=title)
        print(f"  ✨ [HTML 대시보드 보고서]: {html_path}", flush=True)

    if fmt in ["md", "all"]:
        md_path = os.path.join(output_dir, f"chargers_weekly_briefing_{timestamp}.md")
        md_reporter = MarkdownReporter()
        md_reporter.save(md_path, summarized_articles, briefing, title=title)
        latest_md = os.path.join(output_dir, "chargers_briefing_latest.md")
        md_reporter.save(latest_md, summarized_articles, briefing, title=title)
        print(f"  ✨ [Markdown 브리핑 보고서]: {md_path}", flush=True)

    print("\n" + "=" * 65, flush=True)
    print(f"🎉 총 {len(summarized_articles)}건의 기사 전수 분석 및 한국어 보고서 생성이 완료되었습니다!", flush=True)
    print("=" * 65 + "\n", flush=True)


if __name__ == "__main__":
    main()
