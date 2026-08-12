# 👁️ HiddenEye - Web Technology & CVE Vulnerability Hunter

HiddenEye is a modern, modular, dual-engine (CLI & GUI) cybersecurity reconnaissance and vulnerability scanning tool built in Python. It detects web technologies, extracts version signatures, and cross-references them with known CVE databases.

---

##  Features

* **Dual Engine Architecture:** Run it via command-line (CLI) or modern graphical user interface (GUI).
* **Cross-Platform:** Fully compatible with Windows and Linux environments.
* **Smart Detection Engine:** Analyzes HTTP Headers (`Server`), Meta Generator tags, and parses script paths (like jQuery) using Regex and BeautifulSoup.
* **Threat Intelligence Integration:** Automatically queries CVE data using external security APIs.
* **Modern GUI:** Built with `CustomTkinter` featuring a dark mode aesthetic and asynchronous multi-threading (`threading`) to prevent UI freezes.
* **Rich Terminal Output:** Clean, structured tables and colored logs powered by the `rich` library.

---

##  Project Structure

```text
hiddeneye_cli/
│
├── main.py            # CLI entry point
├── gui.py             # Graphical User Interface (CustomTkinter)
├── requirements.txt   # Project dependencies
└── hiddeneye/
    ├── __init__.py
    ├── fetcher.py     # HTTP request handler & WAF bypass
    ├── detector.py    # Technology & version fingerprinting
    ├── cve_scanner.py # CVE database query engine
    └── reporter.py    # Rich CLI reporting module
```

 Installation & Usage
Clone the repository:

```Bash
git clone [https://github.com/EfsaEryesil/HiddenEye-CLI.git](https://github.com/EfsaEryesil/HiddenEye-CLI.git)
cd hiddeneye_cli
Install dependencies:
```
```
Bash
pip install -r requirements.txt
```
Run CLI Mode:
```
Bash
python main.py -u [https://example.com](https://example.com)
```
Run GUI Mode:
```
Bash
python gui.py
```
License
This project is developed for educational and portfolio purposes.



```bash
git add README.md
git commit -m "Add professional README.md documentation"
git push origin main
```
