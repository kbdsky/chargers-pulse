"""Article scraper for fetching and extracting full article text."""

import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


class ArticleScraper:
    """Extracts main content and metadata from article web pages."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {"User-Agent": USER_AGENT}

    def scrape(self, url: str) -> Dict[str, any]:
        """Fetch URL and extract main text."""
        result = {
            "url": url,
            "title": "",
            "text": "",
            "lead_image": "",
            "success": False,
        }

        if not url or not url.startswith("http"):
            return result

        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "nav", "footer", "aside", "header", "form", "noscript", "svg"]):
                tag.decompose()

            # Extract title if missing
            title_tag = soup.find("h1") or soup.find("title")
            if title_tag:
                result["title"] = title_tag.get_text(strip=True)

            # Try to find open graph image
            og_img = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
            if og_img and og_img.get("content"):
                result["lead_image"] = og_img["content"]

            # Target article bodies
            article_body = (
                soup.find("article")
                or soup.find("div", class_=lambda c: c and any(k in c.lower() for k in ["article-body", "story-body", "entry-content", "post-content", "article__body"]))
                or soup.find("main")
            )

            paragraphs = []
            if article_body:
                for p in article_body.find_all("p"):
                    text = p.get_text(strip=True)
                    if len(text) > 30 and not any(k in text.lower() for k in ["subscribe", "copyright", "advertisement", "all rights reserved"]):
                        paragraphs.append(text)
            else:
                for p in soup.find_all("p"):
                    text = p.get_text(strip=True)
                    if len(text) > 40:
                        paragraphs.append(text)

            result["text"] = "\n\n".join(paragraphs[:15])  # Cap at top 15 paragraphs
            result["success"] = bool(result["text"])

        except Exception as e:
            logger.debug(f"Could not scrape {url}: {e}")

        return result
