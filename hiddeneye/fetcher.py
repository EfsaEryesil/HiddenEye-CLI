import requests

class WebFetcher:
    def __init__(self, url, proxy=None):
        self.url = url
        self.proxy = proxy
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def fetch(self):
        proxies_dict = None
        if self.proxy:
            proxies_dict = {
                "http": self.proxy,
                "https": self.proxy
            }
        
        try:
            response = requests.get(self.url, headers=self.headers, proxies=proxies_dict, timeout=10, verify=True)
            return {
                "success": True,
                "url": self.url,
                "headers": response.headers,
                "html": response.text
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }