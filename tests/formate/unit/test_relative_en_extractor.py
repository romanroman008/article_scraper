# tests/unit/test_relative_en_extractor.py
import pytest
from bs4 import BeautifulSoup
from scraper.infrastructure.parsing.date.extract.strategies.relative_en_extractor import RelativeEnTextDateExtractor

soup = lambda h: BeautifulSoup(h, "html.parser")

@pytest.mark.parametrize("html,expected", [
    ('<div class="post-meta">yesterday at 23:59:59</div>', "yesterday at 23:59:59"),
    ('<div class="post-meta">today at 9</div>', "today at 9"),
    ('<div class="entry-meta">Earlier today</div>', "earlier today"),
    ('<div class="entry-meta">This morning</div>', "this morning"),
    ('<div class="entry-meta">Last night</div>', "last night"),
])
def test_en_compounds(html, expected):
    assert RelativeEnTextDateExtractor().extract(soup(html)) == expected

@pytest.mark.parametrize("html,expected", [
    ('<div class="date">45s ago</div>', "45s ago"),
    ('<div class="time">30 sec ago</div>', "30 sec ago"),
    ('<div class="date">5m</div>', "5m"),
    ('<div class="date">2 minutes ago</div>', "2 minutes ago"),
    ('<div class="date">3h</div>', "3h"),
    ('<div class="date">2 hours ago</div>', "2 hours ago"),
    ('<div class="date">1d</div>', "1d"),
    ('<div class="date">3 days ago</div>', "3 days ago"),
    ('<div class="date">1 wk ago</div>', "1 wk ago"),
    ('<div class="date">2 weeks ago</div>', "2 weeks ago"),
    ('<div class="date">1 month ago</div>', "1 month ago"),
    ('<div class="date">3 months ago</div>', "3 months ago"),
    ('<div class="date">1 yr ago</div>', "1 yr ago"),
    ('<div class="date">2 years ago</div>', "2 years ago"),
])
def test_en_units(html, expected):
    assert RelativeEnTextDateExtractor().extract(soup(html)) == expected

@pytest.mark.parametrize("html,expected", [
    ('<div class="date">Yesterday</div>', "yesterday"),
    ('<div class="date">Today</div>', "today"),
    ('<div class="date">Just now</div>', "just now"),
    ('<div class="date">A moment ago</div>', "a moment ago"),
])
def test_en_keywords(html, expected):
    assert RelativeEnTextDateExtractor().extract(soup(html)) == expected
