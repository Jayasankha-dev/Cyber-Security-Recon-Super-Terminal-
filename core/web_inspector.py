import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
import re
import time

class WebInspector:
    def __init__(self, net_callback, js_callback, html_callback, links_callback,
                 status_callback, stop_flag_ref):
        self.net_callback = net_callback
        self.js_callback = js_callback
        self.html_callback = html_callback
        self.links_callback = links_callback
        self.status_callback = status_callback
        self.stop_flag_ref = stop_flag_ref
        self.session = requests.Session()

    def start_analysis(self, target):
        self.status_callback(f"Status: Analyzing '{target}'...", "yellow")
        try:
            # Stop check before starting
            if self.stop_flag_ref():
                self.status_callback("Status: Cancelled by user.", "red")
                return

            # Smart URL detection
            url = self._normalize_target(target)
            self.net_callback(f"[+] Target URL: {url}\n[+] Sending HTTP GET Request...\n")

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            # Use a timeout and allow stopping via a custom event
            response = self._fetch_with_stop(url, headers)
            if response is None:
                return  # stopped or error

            self.net_callback(f"[+] Status Code: {response.status_code}\n\n")

            # 1. Security Headers
            self._analyze_headers(response)

            if response.status_code == 200:
                html = response.text
                self.html_callback(html)

                soup = BeautifulSoup(html, 'html.parser')

                # 2. JavaScript assets
                self._extract_scripts(soup, url)

                # 3. Comments
                self._extract_comments(soup)

                # 4. Forms
                self._extract_forms(soup, url)

                # 5. Links
                self._extract_links(soup, url)

                self.status_callback("Status: Cyber Security Recon & Analysis Complete.", "lime")
            else:
                self.net_callback(f"[-] Error: Received HTTP status code {response.status_code}\n")
                self.status_callback("Status: Analysis Failed.", "red")

        except Exception as e:
            self.net_callback(f"[-] Error: {e}\n", True)
            self.status_callback("Status: Error occurred during analysis.", "red")

    def _normalize_target(self, target):
        # Check if it looks like a URL
        if re.match(r'^https?://', target) or re.match(r'^www\.[a-zA-Z0-9\-]+\.[a-zA-Z]+', target):
            if not target.startswith('http'):
                target = 'https://' + target
            return target
        else:
            # Fallback to Google search
            return f"https://www.google.com/search?q={quote_plus(target)}"

    def _fetch_with_stop(self, url, headers, timeout=15):
        try:
            # We'll use a generator to yield chunks and check stop flag
            # Simpler: just use a timeout and check before and after
            if self.stop_flag_ref():
                self.status_callback("Status: Cancelled by user.", "red")
                return None
            response = self.session.get(url, headers=headers, timeout=timeout)
            # Check after request
            if self.stop_flag_ref():
                self.status_callback("Status: Cancelled after request.", "red")
                return None
            return response
        except requests.exceptions.Timeout:
            self.net_callback("[-] Request timed out.\n", True)
            self.status_callback("Status: Timeout.", "red")
            return None
        except requests.exceptions.RequestException as e:
            self.net_callback(f"[-] Request error: {e}\n", True)
            self.status_callback("Status: Request failed.", "red")
            return None

    def _analyze_headers(self, response):
        self.net_callback("=== SECURITY HEADERS ===\n")
        sec_headers = [
            'Content-Security-Policy', 'Strict-Transport-Security',
            'X-Frame-Options', 'X-Content-Type-Options',
            'X-XSS-Protection', 'Server', 'X-Powered-By'
        ]
        for h in sec_headers:
            val = response.headers.get(h, "Missing / Not Set")
            self.net_callback(f"{h}: {val}\n")

        # Check cookies for secure flags
        cookies = response.cookies
        if cookies:
            self.net_callback("\n=== COOKIES ===\n")
            for cookie in cookies:
                secure = "Secure" if cookie.secure else "Not Secure"
                httponly = "HttpOnly" if cookie.has_nonstandard_attr('HttpOnly') else "Not HttpOnly"
                self.net_callback(f"{cookie.name}: {cookie.value} | {secure} | {httponly}\n")
        self.net_callback("\n")

    def _extract_scripts(self, soup, base_url):
        scripts = soup.find_all('script')
        self.js_callback(f"=== EXTRACTED JAVASCRIPT FILES ({len(scripts)}) ===\n")
        for s in scripts:
            src = s.get('src')
            if src:
                self.js_callback(f"[JS] {urljoin(base_url, src)}\n")

    def _extract_comments(self, soup):
        comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--'))
        self.js_callback(f"\n=== HTML COMMENTS FOUND ({len(comments)}) ===\n")
        for c in comments[:10]:
            self.js_callback(f"[COMMENT] {c.strip()}\n")

    def _extract_forms(self, soup, base_url):
        forms = soup.find_all('form')
        self.links_callback(f"=== INPUT FORMS FOUND ({len(forms)}) ===\n")
        for idx, f in enumerate(forms):
            action = f.get('action', 'N/A')
            method = f.get('method', 'get').upper()
            self.links_callback(f"Form #{idx+1} | Method: {method} | Action: {urljoin(base_url, action)}\n")

    def _extract_links(self, soup, base_url):
        links = soup.find_all('a')
        self.links_callback(f"\n=== TARGET LINKS ({len(links)}) ===\n")
        for l in links[:30]:
            txt = l.get_text(strip=True)
            href = l.get('href')
            if txt and href:
                self.links_callback(f"-> [{txt[:25]}] : {urljoin(base_url, href)}\n")