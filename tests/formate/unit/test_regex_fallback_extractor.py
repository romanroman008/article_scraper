# tests/unit/test_regex_fallback_extractor.py
import pytest
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.strategies.regex_fallback_extractor import RegexFallbackDateExtractor


def make_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def test_returns_numeric_dd_mm_yyyy_when_present():
    html = "<div>Opublikowano: 07.02.2024 o 12:00</div>"
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    assert extractor.extract(soup) == "07.02.2024"

def test_returns_polish_words_when_no_numeric():
    html = "<p>Aktualizacja: 2 stycznia 2024</p>"
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    assert extractor.extract(soup) == "2 stycznia 2024"

def test_ignores_case_and_accents():
    html = "<p>DATA: 15 PAŹDZIERNIKA 2025</p>"
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    # Ekstraktor zwraca lowercase, bo cały tekst obniżamy
    assert extractor.extract(soup) == "15 października 2025"

def test_fallback_priority_numeric_over_words_even_if_words_earlier():
    html = """
    <article>
      <span>2 stycznia 2024</span>
      <span>... później: 03.01.2024</span>
    </article>
    """
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    # Priorytet ma regex numeric (pierwszy w łańcuchu), więc dostaniemy numeric,
    # nawet jeśli słowne wystąpi wcześniej w tekście.
    assert extractor.extract(soup) == "03.01.2024"

def test_none_when_no_match():
    html = "<div>Brak daty tutaj.</div>"
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    assert extractor.extract(soup) is None

def test_word_boundaries_prevent_false_positives():
    # Sprawdzamy, że nie złapiemy fragmentu IP czy liczby z kropkami poza wzorcem.
    html = "<p>Kontakt: 192.168.0.1 — build 1.2.3, ale data to 01.12.2024</p>"
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    assert extractor.extract(soup) == "01.12.2024"

@pytest.mark.parametrize("html,expected", [
    ("<p>1.1.2024</p>", "1.1.2024"),
    ("<p>01.01.2024</p>", "01.01.2024"),
    ("<p>9 wrzesnia 2024</p>", "9 wrzesnia 2024"),  # bez polskich znaków też ma działać
])
def test_parametrized_common_variants(html, expected):
    soup = make_soup(html)
    extractor = RegexFallbackDateExtractor()
    assert extractor.extract(soup) == expected
