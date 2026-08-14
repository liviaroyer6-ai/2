import os
import json
from constants import ASSET_DIR

SESSION_FILE = os.path.join(ASSET_DIR, "session.json")

def save_session(username, progress):
    os.makedirs(ASSET_DIR, exist_ok=True)
    data = {"username": username, "progress": progress}
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"[DEBUG] Session saved for user: {username}")

def load_session():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                print(f"[DEBUG] Session loaded: {data}")
                return data
    except Exception as e:
        print(f"[DEBUG] Error loading session: {e}")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("[DEBUG] Session cleared")
