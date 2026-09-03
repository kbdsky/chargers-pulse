"""Unit tests for news processor (deduplication, categorizer, summarizer, ranker, dynamic keywords, game analyzer)."""

import pytest
from newspulse.processor import (
    Deduplicator,
    Categorizer,
    Summarizer,
    ArticleRanker,
    DynamicKeywordTracker,
    GameAnalyzer,
)


def test_deduplicator():
    articles = [
        {
            "title": "Chargers defeat Raiders in season opener",
            "url": "https://example.com/news1",
            "summary": "Short summary",
        },
        {
            "title": "Chargers defeat Raiders in season opener - highlights",
            "url": "https://example.com/news2",
            "summary": "Longer summary with details",
        },
        {
            "title": "Jim Harbaugh comments on team culture",
            "url": "https://example.com/news3",
            "summary": "Harbaugh interview",
        },
    ]

    dedup = Deduplicator(similarity_threshold=0.6)
    result = dedup.deduplicate(articles)
    assert len(result) == 2
    assert "Raiders" in result[0]["title"]
    assert "Harbaugh" in result[1]["title"]


def test_ranker():
    ranker = ArticleRanker()
    high_impact_art = {
        "title": "Justin Herbert questionable with ankle injury, placed on IR",
        "summary": "Coach Jim Harbaugh announced starter Justin Herbert suffered a severe ankle injury.",
        "source": "ESPN NFL",
        "published": "2026-08-23T10:00:00",
    }
    low_impact_art = {
        "title": "Chargers fan fest photos",
        "summary": "Photos from the event.",
        "source": "Community",
    }

    score_high = ranker.score_article(high_impact_art)
    score_low = ranker.score_article(low_impact_art)

    assert score_high > score_low
    assert high_impact_art["priority_tier"] in ["🚨 긴급/핵심", "⚡ 주요"]


def test_dynamic_keyword_tracker(tmp_path):
    cache_file = tmp_path / "test_keywords.json"
    tracker = DynamicKeywordTracker(cache_file=str(cache_file))

    articles = [
        {
            "title": "Joe Alt dominates in joint practice against 49ers",
            "summary": "Rookie offensive tackle Joe Alt had great reps against San Francisco 49ers.",
        },
        {
            "title": "Chargers vs 49ers preseason game recap",
            "summary": "Preseason week 2 action against 49ers.",
        },
    ]

    trends = tracker.extract_trends_from_articles(articles)
    assert "trending_keywords" in trends
    assert len(trends["trending_keywords"]) > 0


def test_game_analyzer():
    analyzer = GameAnalyzer()
    articles = [
        {
            "title": "Chargers vs. 49ers Preseason Week 2: Niners win 41-17",
            "summary": "Joint practice and preseason match recap against San Francisco 49ers.",
            "category_key": "game",
        }
    ]

    game_data = analyzer.analyze_game_news(articles)
    assert game_data["has_game_data"] is True
    assert "49ers" in game_data["opponent"]
    assert "41-17" in str(game_data["score_detected"])


def test_categorizer():
    categorizer = Categorizer()

    injury_art = {
        "title": "Justin Herbert questionable with ankle injury",
        "summary": "QB Justin Herbert left practice with an injury.",
    }
    cat_injury = categorizer.categorize_article(injury_art)
    assert cat_injury["category_key"] == "injury"
    assert "부상" in cat_injury["category_name"]

    roster_art = {
        "title": "Chargers sign veteran offensive tackle to contract",
        "summary": "New contract extension and free agent signing.",
    }
    cat_roster = categorizer.categorize_article(roster_art)
    assert cat_roster["category_key"] == "roster"

    interview_art = {
        "title": "Coach Jim Harbaugh speaks at press conference",
        "summary": "Harbaugh says the team is working hard.",
    }
    cat_interview = categorizer.categorize_article(interview_art)
    assert cat_interview["category_key"] == "interview"


def test_summarizer():
    summarizer = Summarizer()

    article = {
        "title": "Justin Herbert shines as Jim Harbaugh praises defense in Chargers victory",
        "summary": "The Los Angeles Chargers secured a 24-17 win behind strong quarterback play and rushing.",
        "category_name": "경기 결과",
    }

    sum_art = summarizer.summarize_article(article)
    assert "summary_bullets_kr" in sum_art
    assert len(sum_art["summary_bullets_kr"]) >= 1

    briefing = summarizer.generate_executive_briefing([sum_art])
    assert "headline" in briefing
    assert len(briefing["key_takeaways"]) >= 1
    assert "game_center" in briefing
