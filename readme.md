# 🛡️ Cyber Security Recon & Super Terminal

<img width="1920" height="1080" alt="Capture" src="https://github.com/user-attachments/assets/63de6974-b548-45b6-90c2-37ac95ce4b3b" />


[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)

A powerful, all-in-one **Cyber Security Reconnaissance & Super Terminal** desktop application built with Python and `customtkinter`. It combines a web security inspector, dark-themed GUI.

---

## 🚀 Key Features

- **🌐 Web Security Inspector**
  - Analyzes HTTP security headers (CSP, HSTS, X-Frame-Options, etc.).
  - Extracts JavaScript files and inline scripts.
  - Finds hidden HTML comments (potential info leaks).
  - Enumerates Forms and interactive Links.
  - Displays raw HTML source code with automatic truncation for large pages.
  - Checks Cookie security flags (Secure & HttpOnly).
  - Falls back to Google search if the input is not a URL.

- **💻 Super Terminal**
  - Execute native **CMD** and **PowerShell** commands directly from the UI.
  - Real-time output streaming.
  - Prefix `pwsh:` to run PowerShell commands (e.g., `pwsh: Get-Process`).

- **🖥️ System Utilities**
  - **USB Drive Scanner:** Type `usb` to scan and display storage drives with total/free space.

- **🧠 Smart Command History**
  - Automatically saves your last 50 commands to `cmd_history.json`.
  - Deduplicates entries (moves used commands to the top).

- **⚡ Robust & Safe**
  - **Thread-Safe UI:** All widgets update safely on the main thread—no crashes or flickering.
  - **Stop Button:** Cancel long-running web requests or terminal commands instantly.
  - **Clear All:** Wipe all output panes with one click.
  - **Save Report:** Export all analysis results to a timestamped `.txt` file.

---

## 📸 Application Preview

The application features a 4‑column layout:

```
+-----------------------------------------------------------------------------+
|  [Target / Search / Cmd:] [___________________________] [Run] [Stop] [Clear] [Save] |
+------------------+------------------+------------------+------------------+
|  Security Headers |  JS Files &     |  Forms & Links   |  Raw HTML        |
|  & Logs           |  Comments       |                  |  Source Code     |
|                   |                 |                  |                  |
|  ...              |  ...            |  ...             |  ...             |
+------------------+------------------+------------------+------------------+
| Status: Ready |                                                                 |
+-----------------------------------------------------------------------------+
```

---

## 📦 Tech Stack

- **Python 3.8+**
- **CustomTkinter** – Modern, customizable UI toolkit.
- **Requests** – HTTP client for web analysis.
- **BeautifulSoup4** – HTML parsing and data extraction.
- **Pillow** – Image processing support (used by CustomTkinter).

---

## 🔧 Installation & Setup

1. **Clone or Download** this repository.

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install them manually:*

   ```bash
   pip install customtkinter requests beautifulsoup4 pillow
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

---

## 🎮 How to Use

### 🕵️ Web Reconnaissance
- Type a **URL** (e.g., `https://example.com` or `www.example.com`) in the top bar.
- Type a **Google search query** (e.g., `Sinhala recipes`) to perform a Google search and analyze the results page.
- Click **Run Analysis** (or press `Enter`).
- View the results in the four panels:
  - **Security Headers & Logs:** HTTP response headers and cookie flags.
  - **JS Files & Comments:** Extracted script sources and juicy HTML comments.
  - **Forms & Links:** All input forms and the first 30 links found on the page.
  - **Raw HTML:** The full source code of the page (truncated to 50k chars).

### 💻 Terminal Commands
- Type any **CMD** command (e.g., `ipconfig`, `ping google.com`, `tree`) and press **Run**.
- Type **PowerShell** commands using the `pwsh:` prefix (e.g., `pwsh: Get-Service | Select-Object -First 5`).
- Output will appear in the **Security Headers & Logs** panel.

### 🖥️ USB Scan
- Simply type `usb` and hit **Run**. The drive details will appear in the first panel.

### 🛑 Controls
- **Stop:** Immediately halts the current web request or terminal process.
- **Clear All:** Empties all four output boxes.
- **Save Report:** Saves all current output to `report_YYYYMMDD_HHMMSS.txt` in the project directory.

---

## 📁 Project Structure

```
.
├── main.py                     # Application entry point & main UI
├── cmd_history.json            # Auto-generated command history
├── requirements.txt            # Python dependencies
├── core/
│   ├── __init__.py
│   ├── terminal_runner.py      # Handles CMD and PowerShell execution
│   └── web_inspector.py        # Web crawling, header analysis, and parsing logic
└── utils/
    ├── __init__.py
    └── helpers.py              # History management & USB drive scanning
```

---

## 🧪 Testing & Error Handling

- The application gracefully handles network timeouts, connection errors, and invalid commands.
- The **Stop** button uses a shared flag to interrupt processes safely.
- All exceptions are caught and displayed in the UI with a clear red status message.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Jayasankha-dev/your-repo/issues) if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact

**Jayasankha Madhusith** – [@BenjaminUS](https://twitter.com/madhusith) – k8775.jayasankha@gmail.com

Project Link: [https://github.com/Jayasankha-dev](https://github.com/Jayasankha-dev)

---

**Happy Reconnaissance! 🕵️‍♂️💻**
