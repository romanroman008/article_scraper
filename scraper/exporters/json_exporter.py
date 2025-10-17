# scraper/exporters/json_exporter.py
from pathlib import Path
import json
from typing import Iterable
from scraper.domain.models import ArticleData

class JsonExporter:
    def export(self, articles: Iterable[ArticleData], out_path: str | Path) -> Path:
        data = []
        for a in articles:
            data.append({
                "url": a.url,
                "title": a.title,
                "content_html": a.content_html,
                "content_text": a.content_text,
                "published_at": a.published_at,
                "source_domain": a.source_domain,
            })
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return out_path
