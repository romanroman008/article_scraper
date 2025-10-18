import logging
from typing import Optional

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger("scraper.parsing_utils")


def pick_title(soup: BeautifulSoup) -> str:
    og = soup.find("meta", {"property": "og:title"}) or soup.find("meta", {"name": "twitter:title"})
    if og and og.get("content"):
        title = og["content"].strip()
        logger.info(
            'Wybrano tytuł z meta (strategia=meta, długość=%d, próbka="%s").',
            len(title), title[:120]
        )
        return title

    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
        logger.info(
            'Wybrano tytuł z nagłówka (strategia=h1, długość=%d, próbka="%s").',
            len(title), title[:120]
        )
        return title

    if soup.title:
        title = soup.title.get_text(strip=True)
        logger.info(
            'Wybrano tytuł z <title> (strategia=title-tag, długość=%d, próbka="%s").',
            len(title), title[:120]
        )
        return title

    logger.warning("Nie znaleziono tytułu w meta/h1/title – użyto wartości domyślnej.")
    return "(brak tytułu)"


def pick_container(soup: BeautifulSoup):
    node = soup.select_one("article") or soup.find("main") or soup.body
    if node is not None:
        strategy = node.name if hasattr(node, "name") else "unknown"
        node_id = _safe_attr(node, "id")
        node_cls = _safe_class(node)
        logger.info(
            "Wybrano kontener treści (strategia=%s, id=%s, class=%s).",
            strategy, node_id, node_cls
        )
        return node

    logger.warning("Nie znaleziono kontenera treści (article/main/body).")
    return None


def html_to_text(html_fragment: str) -> str:
    if not html_fragment:
        return ""

    s = BeautifulSoup(html_fragment, "html.parser")
    removed = 0
    for t in s(["script", "style", "noscript"]):
        t.decompose()
        removed += 1

    text = s.get_text("\n", strip=True)
    logger.info(
        'Przekształcono HTML na tekst (usunięto_węzłów=%d, długość=%d, linie=%d, próbka="%s").',
        removed, len(text), (text.count("\n") + 1 if text else 0), text[:160]
    )
    return text



def _safe_attr(tag: Tag, key: str) -> Optional[str]:
    try:
        return tag.get(key)  # type: ignore[call-arg]
    except Exception:
        return None

def _safe_class(tag: Tag) -> Optional[str]:
    try:
        classes = tag.get("class", [])
        return " ".join(classes) if isinstance(classes, (list, tuple)) else str(classes)
    except Exception:
        return None