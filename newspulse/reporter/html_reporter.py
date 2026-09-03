"""HTML Report Generator using Jinja2 templates."""

import os
import datetime
from pathlib import Path
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader


class HTMLReporter:
    """Renders structured article data into modern HTML dashboard reports."""

    def __init__(self, template_dir: str = None):
        if not template_dir:
            template_dir = str(Path(__file__).parent / "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def render(
        self,
        articles: List[Dict[str, any]],
        briefing: Dict[str, any],
        title: str = "LA Chargers 종합 뉴스 인텔리전스 리포트",
    ) -> str:
        """Render HTML string from article and briefing data."""
        template = self.env.get_template("chargers_report.html")

        # Compute stats
        sources = set(art.get("source", "") for art in articles if art.get("source"))
        categories = set(art.get("category_key", "") for art in articles if art.get("category_key"))
        injuries = [art for art in articles if art.get("category_key") == "injury"]
        games = [art for art in articles if art.get("category_key") == "game"]

        stats = {
            "sources_count": len(sources),
            "categories_count": len(categories),
            "injuries_count": len(injuries),
            "games_count": len(games),
        }

        generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return template.render(
            title=title,
            articles=articles,
            briefing=briefing,
            stats=stats,
            generated_at=generated_at,
        )

    def save(
        self,
        output_path: str,
        articles: List[Dict[str, any]],
        briefing: Dict[str, any],
        title: str = "LA Chargers 종합 뉴스 인텔리전스 리포트",
    ) -> str:
        """Render and save HTML report to file."""
        html_content = self.render(articles=articles, briefing=briefing, title=title)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return output_path
