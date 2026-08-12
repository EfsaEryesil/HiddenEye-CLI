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
    parser = argparse.ArgumentParser(description="HiddenEye - Web Teknoloji ve CVE Tarayıcısı")
    parser.add_argument("-u", "--url", required=True, help="Taranacak hedef URL (Örn: https://example.com)")
    args = parser.parse_args()


    with console.status("[bold yellow]Hedef siteye HiddenEye gözü odaklanıyor...[/bold yellow]"):
        fetcher = WebFetcher(args.url)
        fetch_result = fetcher.fetch()

    if not fetch_result["success"]:
        console.print(f"[bold red][!] Bağlantı Hatası:[/bold red] {fetch_result['error']}")
        return


    with console.status("[bold yellow]Teknolojiler ve sürümler taranıyor...[/bold yellow]"):
        detector = TechDetector(fetch_result)
        detected_techs = detector.detect()

    if not detected_techs:
        console.print("[yellow][!] No known technology signatures detected.[/yellow]")
        return

    
    cve_scanner = CVEScanner()
    for tech in detected_techs:
        with console.status("[bold yellow]HiddenEye is locking onto the target...[/bold yellow]"):
            cves = cve_scanner.search_cve(tech["vendor"], tech["product"], tech["version"])
            tech["cves"] = cves

  
    Reporter.print_results(fetch_result["url"], detected_techs)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
    
        console.print("\n[bold red][!] Tarama kullanıcı tarafından iptal edildi. Çıkılıyor...[/bold red]")
        sys.exit(0)