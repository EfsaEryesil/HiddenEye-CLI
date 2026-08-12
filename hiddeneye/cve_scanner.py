import requests

class CVEScanner:
    def __init__(self):
        self.api_url = "https://cve.circl.lu/api/search/"

    def search_cve(self, vendor: str, product: str, version: str):
        if version == "Bilinmiyor":
            return []

        target_endpoint = f"{self.api_url}{vendor}/{product}"
        cve_results = []

        try:
            response = requests.get(target_endpoint, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", []):
                    summary = item.get("summary", "")
                    cve_id = item.get("id", "")
                    cvss = item.get("cvss", "N/A")

                    if version in summary:
                        cve_results.append({
                            "id": cve_id,
                            "cvss": cvss,
                            "summary": summary[:110] + "..."
                        })
                        
                    if len(cve_results) >= 3:
                        break
        except Exception:
            pass

        return cve_results