"""Unit tests for HTML and Markdown reporters."""

import os
import pytest
from newspulse.reporter import HTMLReporter, MarkdownReporter


def test_reporters_render_and_save(tmp_path):
    articles = [
        {
            "title": "Chargers announce starting lineup",
            "url": "https://example.com/lineup",
            "summary": "Starting lineup for the upcoming game.",
            "source": "Chargers Wire",
            "published": "2026-08-23T12:00:00",
            "category_key": "roster",
            "category_badge": "🎯 영입/계약",
            "category_name": "계약/트레이드/드래프트",
            "headline_kr": "[로스터] Chargers announce starting lineup",
            "summary_bullets_kr": ["선수 명단 발표", "핵심 스타터 확정"],
        }
    ]

    briefing = {
        "headline": "⚡ LA 차저스 최신 팀 뉴스 브리핑",
        "key_takeaways": ["총 1건의 기사 수집", "선수단 라인업 확정"],
        "injury_update": "특이사항 없음",
        "team_outlook": "팀 분위기 양호",
    }

    # HTML Reporter Test
    html_reporter = HTMLReporter()
    html_out = html_reporter.render(articles, briefing, title="테스트 보고서")
    assert "<!DOCTYPE html>" in html_out
    assert "LA CHARGERS" in html_out
    assert "테스트 보고서" in html_out

    html_file = tmp_path / "test_report.html"
    html_reporter.save(str(html_file), articles, briefing)
    assert os.path.exists(html_file)

    # Markdown Reporter Test
    md_reporter = MarkdownReporter()
    md_out = md_reporter.render(articles, briefing, title="⚡ 테스트 보고서")
    assert "# ⚡ 테스트 보고서" in md_out
    assert "선수단 라인업 확정" in md_out

    md_file = tmp_path / "test_report.md"
    md_reporter.save(str(md_file), articles, briefing)
    assert os.path.exists(md_file)
