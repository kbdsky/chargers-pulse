"""News collectors for RSS, Google News, and Web Scraping."""

from .rss import RSSCollector
from .google_news import GoogleNewsCollector
from .scraper import ArticleScraper

__all__ = ["RSSCollector", "GoogleNewsCollector", "ArticleScraper"]
