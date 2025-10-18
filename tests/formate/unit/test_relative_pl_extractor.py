# tests/unit/test_relative_pl_extractor.py
import pytest
from bs4 import BeautifulSoup

from scraper.infrastructure.parsing.date.extract.strategies.relative_time_pl_extractor import \
    RelativePlTextDateExtractor

soup = lambda h: BeautifulSoup(h, "html.parser")

@pytest.mark.parametrize("html,expected", [
    ('<div class="post-meta">wczoraj o 13:00</div>', "wczoraj o 13:00"),
    ('<div class="post-meta">dziś o 9.30</div>', "dziś o 9.30"),
    ('<div class="entry-meta">Dzisiaj wcześniej</div>', "dzisiaj wcześniej"),
    ('<div class="entry-meta">Dziś wieczorem</div>', "dziś wieczorem"),
    ('<div class="entry-meta">Wczoraj w nocy</div>', "wczoraj w nocy"),
])
def test_pl_compounds(html, expected):
    assert RelativePlTextDateExtractor().extract(soup(html)) == expected

@pytest.mark.parametrize("html,expected", [
    ('<div class="time">1 sek. temu</div>', "1 sek. temu"),
    ('<div class="time">10 sekund temu</div>', "10 sekund temu"),
    ('<div class="date">15 min</div>', "15 min"),
    ('<div class="date">1 minutę temu</div>', "1 minutę temu"),
    ('<div class="date">3 minuty wstecz</div>', "3 minuty wstecz"),
    ('<div class="date">3h</div>', "3h"),
    ('<div class="date">3 godz. temu</div>', "3 godz. temu"),
    ('<div class="date">2 dni temu</div>', "2 dni temu"),
    ('<div class="date">sprzed 4 dni</div>', "sprzed 4 dni"),
    ('<div class="date">1 tydzień temu</div>', "1 tydzień temu"),
    ('<div class="date">sprzed 3 tygodni</div>', "sprzed 3 tygodni"),
    ('<div class="date">1 miesiąc temu</div>', "1 miesiąc temu"),
    ('<div class="date">sprzed 2 miesięcy</div>', "sprzed 2 miesięcy"),
    ('<div class="date">sprzed 2 miesiecy</div>', "sprzed 2 miesiecy"),
    ('<div class="date">1 rok temu</div>', "1 rok temu"),
    ('<div class="date">sprzed 5 lat</div>', "sprzed 5 lat"),
])
def test_pl_units(html, expected):
    assert RelativePlTextDateExtractor().extract(soup(html)) == expected

@pytest.mark.parametrize("html,expected", [
    ('<div class="date">Wczoraj</div>', "wczoraj"),
    ('<div class="date">Dzisiaj</div>', "dzisiaj"),
    ('<div class="date">Dziś</div>', "dziś"),
    ('<div class="date">przed chwilą</div>', "przed chwilą"),
    ('<div class="date">chwile temu</div>', "chwile temu"),
])
def test_pl_keywords(html, expected):
    assert RelativePlTextDateExtractor().extract(soup(html)) == expected
