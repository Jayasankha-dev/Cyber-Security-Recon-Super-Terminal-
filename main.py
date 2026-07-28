import threading
import customtkinter as ctk
from datetime import datetime
import os
import re

from core.terminal_runner import TerminalRunner
from core.web_inspector import WebInspector
from utils.helpers import load_history, save_history

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SuperTerminalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CYBER SECURITY RECON & SUPER TERMINAL")
        self.geometry("1300x800")

        self.history = load_history()
        self.stop_flag = False          # Used to cancel ongoing operations

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top Control Bar ---
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.mode_label = ctk.CTkLabel(self.top_frame, text="Target / Search ", font=("Arial", 12, "bold"))
        self.mode_label.pack(side="left", padx=10, pady=10)

        self.cmd_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Enter URL or Google query", width=600)
        self.cmd_entry.pack(side="left", padx=5, pady=10)
        self.cmd_entry.bind("<Return>", lambda e: self.execute_action())

        self.run_btn = ctk.CTkButton(self.top_frame, text="Run Analysis", command=self.execute_action)
        self.run_btn.pack(side="left", padx=5, pady=10)

        self.stop_btn = ctk.CTkButton(self.top_frame, text="Stop", command=self.stop_operation, fg_color="red", hover_color="#8B0000")
        self.stop_btn.pack(side="left", padx=5, pady=10)

        self.clear_btn = ctk.CTkButton(self.top_frame, text="Clear All", command=self.clear_all, fg_color="gray")
        self.clear_btn.pack(side="left", padx=5, pady=10)

        self.save_btn = ctk.CTkButton(self.top_frame, text="Save Report", command=self.save_report, fg_color="#2E8B57")
        self.save_btn.pack(side="left", padx=5, pady=10)

        # --- Multi-Column Layout ---
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # 1. Network & Security Headers
        ctk.CTkLabel(self.content_frame, text="Security Headers & Logs", font=("Arial", 11, "bold"), text_color="cyan").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.net_box = ctk.CTkTextbox(self.content_frame, font=("Consolas", 10))
        self.net_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 2. JavaScript & Comments
        ctk.CTkLabel(self.content_frame, text="JS Files & Source Comments", font=("Arial", 11, "bold"), text_color="yellow").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.js_box = ctk.CTkTextbox(self.content_frame, font=("Consolas", 10))
        self.js_box.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 3. Forms & Links
        ctk.CTkLabel(self.content_frame, text="Forms & Target Links", font=("Arial", 11, "bold"), text_color="orange").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.links_box = ctk.CTkTextbox(self.content_frame, font=("Consolas", 10))
        self.links_box.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # 4. HTML Source Code
        ctk.CTkLabel(self.content_frame, text="Raw HTML Source Code", font=("Arial", 11, "bold"), text_color="lime").grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.html_box = ctk.CTkTextbox(self.content_frame, font=("Consolas", 10))
        self.html_box.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)

        # --- Status Bar ---
        self.status_bar = ctk.CTkLabel(self, text="Status: Ready | Type a target URL or search query.", anchor="w", text_color="gray")
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 5))

        # --- Initialize Modules (with thread-safe callbacks) ---
        self.web_inspector = WebInspector(
            net_callback=self._safe_insert(self.net_box),
            js_callback=self._safe_insert(self.js_box),
            html_callback=self._safe_load_html,
            links_callback=self._safe_insert(self.links_box),
            status_callback=self._safe_status_update,
            stop_flag_ref=lambda: self.stop_flag
        )

        self.terminal_runner = TerminalRunner(
            output_callback=self._safe_insert(self.net_box),
            status_callback=self._safe_status_update,
            stop_flag_ref=lambda: self.stop_flag
        )

    # ---------- Thread-safe helpers ----------
    def _safe_insert(self, widget):
        """Return a callback that inserts text into the given widget on the main thread."""
        def callback(text, is_error=False):
            self.after(0, lambda: widget.insert("end", text))
        return callback

    def _safe_load_html(self, html):
        """Load HTML content safely (truncate if too large)."""
        MAX_HTML = 50000
        if len(html) > MAX_HTML:
            html = html[:MAX_HTML] + "\n\n... (truncated, too large)"
        self.after(0, lambda: self.html_box.delete("0.0", "end") or self.html_box.insert("end", html))

    def _safe_status_update(self, text, color):
        """Update status bar safely."""
        self.after(0, lambda: self.status_bar.configure(text=text, text_color=color))

    # ---------- UI Commands ----------
    def stop_operation(self):
        """Set stop flag to cancel ongoing tasks."""
        self.stop_flag = True
        self.update_status("Status: Stop requested...", "orange")

    def clear_all(self):
        """Clear all output boxes."""
        for box in (self.net_box, self.js_box, self.links_box, self.html_box):
            self.after(0, lambda b=box: b.delete("0.0", "end"))
        self.update_status("Status: Cleared all outputs.", "gray")

    def save_report(self):
        """Save all visible output to a timestamped file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=== SECURITY HEADERS & LOGS ===\n")
                f.write(self.net_box.get("0.0", "end"))
                f.write("\n=== JS FILES & COMMENTS ===\n")
                f.write(self.js_box.get("0.0", "end"))
                f.write("\n=== FORMS & LINKS ===\n")
                f.write(self.links_box.get("0.0", "end"))
                f.write("\n=== HTML SOURCE ===\n")
                f.write(self.html_box.get("0.0", "end"))
            self.update_status(f"Status: Report saved as {filename}", "lime")
        except Exception as e:
            self.update_status(f"Status: Failed to save report: {e}", "red")

    def update_status(self, text, color):
        """Direct status update (thread-safe)."""
        self.after(0, lambda: self.status_bar.configure(text=text, text_color=color))

    # ---------- Main Action ----------
    def execute_action(self):
        text = self.cmd_entry.get().strip()
        if not text:
            return

        # Reset stop flag
        self.stop_flag = False

        # Save history
        self.history = save_history(text, self.history)

        # Clear previous output
        self.clear_all()

        # Run Web Analysis directly for any entered target/query
        threading.Thread(target=lambda: self.web_inspector.start_analysis(text), daemon=True).start()

if __name__ == "__main__":
    app = SuperTerminalApp()
    app.mainloop()