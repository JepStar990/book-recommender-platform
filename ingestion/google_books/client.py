import requests
import time
from typing import Dict, Any

BASE_URL = "https://www.googleapis.com/books/v1/volumes"

from typing import Optional

class GoogleBooksClient:
    def __init__(self, api_key: Optional[str] = None, rate_limit_sec: float = 0.2):
        self.api_key = api_key
        self.rate_limit_sec = rate_limit_sec

    def search(self, query: str, start_index: int = 0, max_results: int = 40) -> Dict[str, Any]:
        params = {
            "q": query,
            "startIndex": start_index,
            "maxResults": max_results
        }
        if self.api_key:
            params["key"] = self.api_key

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        time.sleep(self.rate_limit_sec)
        return response.json()
