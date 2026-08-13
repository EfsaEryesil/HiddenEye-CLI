#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from hiddeneye.fetcher import WebFetcher
from hiddeneye.detector import TechDetector
from hiddeneye.cve_scanner import CVEScanner
from hiddeneye.reporter import Reporter
from rich.console import Console

console = Console()

BANNER = """
[bold red]
 █░░█ ░▀░ █▀▀▄ █▀▀▄ █▀▀ █▀▀▄ █▀▀ █░░█ █▀▀ 
 █▀▀█ ▀█▀ █░░█ █░░█ █▀▀ █░░█ █▀▀ █▄▄█ █▀▀ 
 ▀░░▀ ▀▀▀ ▀▀▀░ ▀▀▀░ ▀▀▀ ▀░░▀ ▀▀▀ ▄▄▄▀ ▀▀▀ 
[/bold red]
[bold white]   -- Web Technology and CVE Vulnerability Hunter --[/bold white]
"""

def main():
    console.print(BANNER)
    parser = argparse.ArgumentParser(description="HiddenEye - Web Technology and CVE Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan (e.g., https://example.com)")
    
    # New Proxy parameter
    parser.add_argument("-p", "--proxy", required=False, help="Optional Proxy address (e.g., http://127.0.0.1:8080)")
    
    args = parser.parse_args()

    with console.status("[bold yellow]HiddenEye is focusing on the target site...[/bold yellow]"):
        
        fetcher = WebFetcher(args.url, proxy=args.proxy)
        fetch_result = fetcher.fetch()

    if not fetch_result["success"]:
        console.print(f"[bold red][!] Connection Error:[/bold red] {fetch_result['error']}")
        return

    with console.status("[bold yellow]Scanning technologies and versions...[/bold yellow]"):
        detector = TechDetector(fetch_result)
        detected_techs = detector.detect()

    if not detected_techs:
        console.print("[yellow][!] No known technology signatures detected.[/yellow]")
        return
    
    cve_scanner = CVEScanner()
    for tech in detected_techs:
        with console.status(f"[bold yellow]HiddenEye is locking onto the target: {tech.get('vendor', 'Unknown')}...[/bold yellow]"):
            cves = cve_scanner.search_cve(tech.get("vendor", ""), tech.get("product", ""), tech.get("version", ""))
            tech["cves"] = cves
  
    Reporter.print_results(fetch_result["url"], detected_techs)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Scan cancelled by user. Exiting...[/bold red]")
        sys.exit(0)