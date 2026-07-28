import os
import json

# Use a fixed path relative to this file (go up one level to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "cmd_history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(command, history_list):
    if command in history_list:
        history_list.remove(command)
    history_list.insert(0, command)
    history_list = history_list[:50]   # keep last 50

    # Ensure data directory exists
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_list, f, indent=4)
    except Exception:
        pass
        
    return history_list