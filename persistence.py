import os
import json
from constants import USER_FILE, LEVELS
from constants import USER_FILE, ASSET_DIR

def save_users(users):
    # Ordner anlegen, falls nicht vorhanden
    os.makedirs(ASSET_DIR, exist_ok=True)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    os.makedirs(ASSET_DIR, exist_ok=True)
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(u, p):
    u = str(u)  # Ensure username is always a string
    users = load_users()
    if u in users:
        return False, "❌ Benutzer existiert schon!"
    users[u] = {"password": p, "progress": {"last": 1, "completed": []}}
    save_users(users)
    return True, "✅ Registrierung erfolgreich!"

def login_user(u, p):
    u = str(u).strip()  # Ensure username is always a string and strip whitespace
    p = str(p).strip()  # Ensure password is always a string and strip whitespace

    if not u or not p:  # Check if either field is empty
        return False, "❌ Benutzername und Passwort dürfen nicht leer sein!"

    users = load_users()
    if u in users and users[u]["password"] == p:
        progress = users[u].get("progress", {"last": 1, "completed": []})
        # Validate progress structure
        if not isinstance(progress, dict) or "last" not in progress or "completed" not in progress:
            progress = {"last": 1, "completed": []}
        return True, progress
    return False, "❌ Login fehlgeschlagen!"

def save_progress(current_user, level, prog):
    print(f"[DEBUG] save_progress called with user:{current_user}, level:{level}, prog:{prog}")
    
    if not current_user:
        print("[DEBUG] save_progress: No current user!")
        return False
        
    users = load_users()
    if current_user not in users:
        print(f"[DEBUG] save_progress: User {current_user} not found!")
        return False

    # Get current progress
    user_progress = users[current_user]["progress"]
    
    # Update completed levels if not already completed
    if level not in user_progress["completed"]:
        user_progress["completed"].append(level)
        
    # Update last available level
    user_progress["last"] = max(user_progress["last"], level + 1)
    
    # Save changes
    save_users(users)
    
    # Update the progress parameter to reflect changes
    prog["completed"] = user_progress["completed"]
    prog["last"] = user_progress["last"]
    
    print(f"[DEBUG] save_progress: Successfully saved progress: {user_progress}")
    return True