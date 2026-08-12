import threading
import customtkinter as ctk
from hiddeneye.fetcher import WebFetcher
from hiddeneye.detector import TechDetector
from hiddeneye.cve_scanner import CVEScanner


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class HiddenEyeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

       
        self.title("👁️ HiddenEye - Web Technology & Vulnerability Scanner")
        self.geometry("800x600")
        self.resizable(False, False)

        
        self.title_label = ctk.CTkLabel(
            self, 
            text="HIDDENEYE", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#FF3333"
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Web Teknoloji ve CVE Zafiyet Avcısı", 
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 20))

        
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=40, pady=10)

        self.url_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Taranacak URL'yi girin (Örn: https://example.com)", 
            width=520,
            height=40
        )
        self.url_entry.pack(side="left", padx=(10, 10), pady=10)

        self.scan_button = ctk.CTkButton(
            self.input_frame, 
            text="Taramayı Başlat", 
            command=self.start_scan_thread,
            width=140,
            height=40,
            font=ctk.CTkFont(weight="bold")
        )
        self.scan_button.pack(side="right", padx=(0, 10), pady=10)

        
        self.status_label = ctk.CTkLabel(self, text="Hazır - Hedef URL girin.", text_color="#AAAAAA")
        self.status_label.pack(anchor="w", padx=40, pady=(5, 5))

        
        self.result_box = ctk.CTkTextbox(self, width=720, height=360, font=ctk.CTkFont(family="Consolas", size=13))
        self.result_box.pack(padx=40, pady=10)
        self.result_box.configure(state="disabled")

    def log(self, text):
        """Sonuç kutusuna yazı ekler."""
        self.result_box.configure(state="normal")
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")
        self.result_box.configure(state="disabled")

    def clear_log(self):
        """Sonuç kutusunu temizler."""
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.configure(state="disabled")

    def start_scan_thread(self):
        """Arayüzün donmaması için taramayı arka planda (Thread) çalıştırır."""
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="❌ Lütfen geçerli bir URL girin!", text_color="#FF4444")
            return

        self.scan_button.configure(state="disabled")
        self.clear_log()
        
        
        threading.Thread(target=self.run_scan, args=(url,), daemon=True).start()

    def run_scan(self, url):
        self.status_label.configure(text="🌐 Hedef siteye bağlanılıyor...", text_color="#FFCC00")
        self.log(f"[+] HiddenEye Taraması Başlatıldı: {url}\n" + "="*60)

        # 1. Fetcher
        fetcher = WebFetcher(url)
        fetch_result = fetcher.fetch()

        if not fetch_result["success"]:
            self.log(f"\n[!] Bağlantı Hatası: {fetch_result['error']}")
            self.status_label.configure(text="❌ Bağlantı Başarısız!", text_color="#FF4444")
            self.scan_button.configure(state="normal")
            return

        # 2. Detector
        self.status_label.configure(text="🔍 Teknolojiler ve sürümler taranıyor...", text_color="#FFCC00")
        detector = TechDetector(fetch_result)
        detected_techs = detector.detect()

        if not detected_techs:
            self.log("\n[!] Sitede bilinen bir teknoloji imzası yakalanamadı.")
            self.status_label.configure(text="⚠️ İmzayla eşleşen teknoloji bulunamadı.", text_color="#FFCC00")
            self.scan_button.configure(state="normal")
            return

        # 3. CVE Scanner & Output
        cve_scanner = CVEScanner()
        for tech in detected_techs:
            self.status_label.configure(text=f"🛡️ {tech['name']} için CVE veritabanı taranıyor...", text_color="#FFCC00")
            cves = cve_scanner.search_cve(tech["vendor"], tech["product"], tech["version"])
            
            self.log(f"\n📌 Teknoloji: {tech['name']} (Sürüm: {tech['version']})")
            if not cves:
                self.log("   └─ [Temiz] Bilinen bir güvenlik açığı bulunamadı.")
            else:
                for c in cves:
                    self.log(f"   └─ 🚨 {c['id']} (CVSS: {c['cvss']})")
                    self.log(f"      Özet: {c['summary']}")

        self.log("\n" + "="*60 + "\n[+] Tarama Tamamlandı!")
        self.status_label.configure(text="✅ Tarama Başarıyla Tamamlandı!", text_color="#00FF66")
        self.scan_button.configure(state="normal")

if __name__ == "__main__":
    app = HiddenEyeGUI()
    app.mainloop()