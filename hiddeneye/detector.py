import re
from bs4 import BeautifulSoup

class TechDetector:
    def __init__(self, fetch_result):
        self.headers = fetch_result.get("headers", {})
        self.html = fetch_result.get("html", "")
        self.url = fetch_result.get("url", "")

    def detect(self):
        detected = []
        
        server_header = self.headers.get("Server", "")
        powered_by = self.headers.get("X-Powered-By", "")
        combined_headers = f"{server_header} {powered_by}"
        
        
        if "nginx" in combined_headers.lower():
            version_match = re.search(r"nginx/([0-9.]+)", combined_headers, re.IGNORECASE)
            version = version_match.group(1) if version_match else "Unknown"
            detected.append({"vendor": "f5", "product": "nginx", "version": version})
            
        
        elif "apache" in combined_headers.lower():
            version_match = re.search(r"Apache/([0-9.]+)", combined_headers, re.IGNORECASE)
            version = version_match.group(1) if version_match else "Unknown"
            detected.append({"vendor": "apache", "product": "http_server", "version": version})
            
        
        elif "microsoft-iis" in combined_headers.lower() or "iis" in combined_headers.lower():
            version_match = re.search(r"IIS/([0-9.]+)", combined_headers, re.IGNORECASE)
            version = version_match.group(1) if version_match else "Unknown"
            detected.append({"vendor": "microsoft", "product": "iis", "version": version})
            
       
        if "cloudflare" in combined_headers.lower():
            detected.append({"vendor": "cloudflare", "product": "cloudflare", "version": "Unknown"})

        
        if "php" in powered_by.lower():
            version_match = re.search(r"PHP/([0-9.]+)", powered_by, re.IGNORECASE)
            version = version_match.group(1) if version_match else "Unknown"
            detected.append({"vendor": "php", "product": "php", "version": version})

        
        soup = BeautifulSoup(self.html, "html.parser")
        
       
        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and generator.get("content"):
            content_val = generator["content"]
            if "wordpress" in content_val.lower():
                version_match = re.search(r"WordPress\s+([0-9.]+)", content_val, re.IGNORECASE)
                version = version_match.group(1) if version_match else "Unknown"
                detected.append({"vendor": "wordpress", "product": "wordpress", "version": version})

        
        scripts = soup.find_all("script")
        jquery_detected = False
        react_detected = False
        vue_detected = False

        for script in scripts:
            src = script.get("src", "")
            
           
            if "jquery" in src and not jquery_detected:
                version_match = re.search(r"jquery-([0-9.]+)", src, re.IGNORECASE)
                if not version_match:
                    version_match = re.search(r"/([0-9.]+)/jquery", src, re.IGNORECASE)
                version = version_match.group(1) if version_match else "Unknown"
                detected.append({"vendor": "jquery", "product": "jquery", "version": version})
                jquery_detected = True
                
          
            elif ("react" in src or "react.production" in src) and not react_detected:
                version_match = re.search(r"react@([0-9.]+)", src, re.IGNORECASE)
                version = version_match.group(1) if version_match else "Unknown"
                detected.append({"vendor": "facebook", "product": "react", "version": version})
                react_detected = True
                
           
            elif "vue" in src and not vue_detected:
                version_match = re.search(r"vue@([0-9.]+)", src, re.IGNORECASE)
                version = version_match.group(1) if version_match else "Unknown"
                detected.append({"vendor": "vuejs", "product": "vue", "version": version})
                vue_detected = True

        
        page_text = self.html[:5000].lower()
        if "bootstrap" in page_text:
            detected.append({"vendor": "getbootstrap", "product": "bootstrap", "version": "Unknown"})

        return detected