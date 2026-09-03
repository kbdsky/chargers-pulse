"""Unit tests for news collectors."""

import pytest
from unittest.mock import patch, MagicMock
from newspulse.collector import RSSCollector, GoogleNewsCollector, ArticleScraper


def test_rss_collector_clean_html():
    raw = "<p>Hello <b>Chargers</b> fans! <a href='test'>Click here</a></p>"
    cleaned = RSSCollector._clean_html(raw)
    assert cleaned == "Hello Chargers fans! Click here"


def test_google_news_build_url():
    gnews = GoogleNewsCollector(hl="en-US", gl="US", ceid="US:en")
    url = gnews.build_url("Los Angeles Chargers")
    assert "https://news.google.com/rss/search?q=Los%20Angeles%20Chargers" in url
    assert "&hl=en-US" in url


@patch("requests.get")
def test_rss_collector_fetch_feed_mock(mock_get):
    sample_rss = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Chargers Wire</title>
            <link>https://chargerswire.usatoday.com</link>
            <item>
                <title>Justin Herbert throws 3 TDs in Chargers win</title>
                <link>https://chargerswire.usatoday.com/article/1</link>
                <description>Great performance by Justin Herbert and Jim Harbaugh.</description>
            </item>
        </channel>
    </rss>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = sample_rss.encode("utf-8")
    mock_get.return_value = mock_response

    collector = RSSCollector()
    items = collector.fetch_feed("https://mockfeed.url", source_name="Chargers Wire", limit=5)
    assert len(items) == 1
    assert items[0]["title"] == "Justin Herbert throws 3 TDs in Chargers win"
    assert items[0]["source"] == "Chargers Wire"
    assert "Justin Herbert" in items[0]["summary"]
