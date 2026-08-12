from rich.console import Console
from rich.table import Table

console = Console()

class Reporter:
    @staticmethod
    def print_results(target_url, tech_data):
        console.print(f"\n[bold green][+] HiddenEye Tarama Tamamlandı:[/bold green] {target_url}\n")

        table = Table(title="👁️ HiddenEye Vulnerability Report", show_lines=True)
        table.add_column("Technology", style="cyan", no_wrap=True)
        table.add_column("Version", style="magenta")
        table.add_column("Detected CVEs", style="red")
        for tech in tech_data:
            cves = tech.get("cves", [])
            if not cves:
                cve_text = "[bold green]Clean / No Vulnerabilities Found[/bold green]"
            else:
                cve_text = ""
                for c in cves:
                    cve_text += f"[bold red]• {c['id']}[/bold red] (CVSS: {c['cvss']})\n{c['summary']}\n\n"

            table.add_row(tech["name"], tech["version"], cve_text.strip())

        console.print(table)