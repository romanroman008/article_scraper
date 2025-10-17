
from playwright.sync_api import sync_playwright

class PlaywrightRenderer:
    def render(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0")
            page.goto(url, wait_until="networkidle")
            html = page.content()
            browser.close()
        return html
