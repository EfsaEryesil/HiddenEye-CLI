import requests
from bs4 import BeautifulSoup

class WebFetcher:
    def __init__(self, target_url: str, timeout: int = 10):
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url
        self.url = target_url
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HiddenEye-Scanner/1.0"
        }

    def fetch(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            return {
                "success": True,
                "url": response.url,
                "status_code": response.status_code,
                "headers": response.headers,
                "html": response.text,
                "soup": soup
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }