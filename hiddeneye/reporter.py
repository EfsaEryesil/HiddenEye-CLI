from rich.console import Console
from rich.table import Table

class Reporter:
    @staticmethod
    def print_results(url, detected_techs):
        console = Console()
        console.print(f"\n[bold green][+] HiddenEye Scan Completed:[/bold green] [bold cyan]{url}[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Vendor / Product", style="cyan", width=25)
        table.add_column("Version", style="green", width=15)
        table.add_column("Vulnerabilities (CVEs)", style="red")
        
        for tech in detected_techs:
           
            vendor = tech.get("vendor", "Unknown").capitalize()
            product = tech.get("product", "Unknown").capitalize()
            tech_name = f"{vendor} / {product}" if vendor != product else product
            
            version = tech.get("version", "Unknown")
            
            
            cves = tech.get("cves", [])
            if isinstance(cves, list) and cves:
                cve_text = ", ".join(cves)
            else:
                cve_text = "None Found"
                
            table.add_row(tech_name, version, cve_text)
            
        console.print(table)
        console.print("\n")