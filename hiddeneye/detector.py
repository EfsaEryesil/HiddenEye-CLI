import re

class TechDetector:
    def __init__(self, fetch_data):
        self.headers = fetch_data.get("headers", {})
        self.html = fetch_data.get("html", "")
        self.soup = fetch_data.get("soup")

    def detect(self):
        results = []

       
        server_header = self.headers.get("Server", "")
        if "Apache" in server_header:
            version = self._extract_version(r"Apache/([0-9.]+)", server_header)
            results.append({"name": "Apache HTTP Server", "version": version, "vendor": "apache", "product": "http_server"})

        if "nginx" in server_header.lower():
            version = self._extract_version(r"nginx/([0-9.]+)", server_header)
            results.append({"name": "nginx", "version": version, "vendor": "f5", "product": "nginx"})

        
        meta_gen = self.soup.find("meta", attrs={"name": "generator"}) if self.soup else None
        if meta_gen and "WordPress" in meta_gen.get("content", ""):
            version = self._extract_version(r"WordPress ([0-9.]+)", meta_gen.get("content", ""))
            results.append({"name": "WordPress", "version": version, "vendor": "wordpress", "product": "wordpress"})

      
        jquery_match = re.search(r"jquery[.-]([0-9.]+)(?:\.min)?\.js", self.html, re.IGNORECASE)
        if jquery_match:
            version = jquery_match.group(1)
            results.append({"name": "jQuery", "version": version, "vendor": "jquery", "product": "jquery"})

        return results

    def _extract_version(self, pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else "Bilinmiyor"