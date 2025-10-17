# scraper/infra/parsing_utils.py
from bs4 import BeautifulSoup

def pick_title(soup: BeautifulSoup) -> str:
    og = soup.find("meta", {"property":"og:title"}) or soup.find("meta", {"name":"twitter:title"})
    if og and og.get("content"): return og["content"].strip()
    h1 = soup.find("h1")
    if h1: return h1.get_text(strip=True)
    if soup.title: return soup.title.get_text(strip=True)
    return "(brak tytułu)"

def pick_container(soup: BeautifulSoup):
    return soup.select_one("article") or soup.find("main") or soup.body

def html_to_text(html_fragment: str) -> str:
    s = BeautifulSoup(html_fragment, "html.parser")
    for t in s(["script","style","noscript"]): t.decompose()
    return s.get_text("\n", strip=True)
