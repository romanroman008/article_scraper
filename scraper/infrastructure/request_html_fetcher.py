# scraper/infra/http_client.py
import requests, os
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

HEADERS = {"User-Agent": "Mozilla/5.0"}
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))

class RequestsHtmlFetcher:
    def __init__(self):
        s = requests.Session()
        retry = Retry(total=3, backoff_factor=0.6,
                      status_forcelist=(429,500,502,503,504),
                      allowed_methods=("GET",))
        s.mount("http://", HTTPAdapter(max_retries=retry))
        s.mount("https://", HTTPAdapter(max_retries=retry))
        s.headers.update(HEADERS)
        self._s = s

    def fetch(self, url: str) -> str:
        r = self._s.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
