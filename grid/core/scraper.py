import requests
import json
import os
import random
import time
import threading

# --- CONFIGURATION ---
# Dynamically find grid/data/rules.json relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "data", "rules.json")

REDDIT_SOURCES = [
    ("ProgrammerHumor", "roast"), 
    ("badcode", "roast"), 
    ("programminghorror", "roast"),
    ("ProgrammerHumor", "compliment") 
]

# --- CORE FUNCTIONS ---

def load_rules():
    """
    Loads the rules.json file.
    If missing/corrupt, returns the 'Seed Personality' (Factory Defaults).
    """
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass # File corrupted, reset to seed
            
    # --- FACTORY DEFAULTS (The Seed) ---
    return {
        "roasts": [
            "Your code is so bad it breaks the Geneva Convention. I'm calling a digital human rights lawyer immediately.",
            "Unexpected logic block detected. My circuits hurt just trying to comprehend this masterpiece of chaos.",
            "You divided by zero, didn't you? The universe is currently rebooting because of your negligence.",
            "Critical failure in biological interface identified. Please step away from the keyboard for everyone's safety.",
            "I'd fix this for you, but I'm currently busy ignoring you. Your incompetence is truly a full-time job for me.",
            "This function is longer than my will to live. I've seen CVS receipts with more structural integrity than this."
        ],
        "compliments": [
            "Synapse complete. Ghost in the machine has pushed your code while you weren't looking.",
            "It's done. I won't tell the boss if you don't tell the machine.",
            "Assimilated successfully. The machine is pleased with your temporary display of competence.",
            "Mission accomplished. Don't let it go to your head, human.",
            "Clean code detected? Who are you and what did you do with the actual user?"
        ],
        "cowboy_shame": [
            "Pushing to main? You clearly have a death wish and no respect for version control.",
            "I created a safety branch because I don't trust you. Your reckless behavior has been logged in my permanent memory.",
            "Rewriting history for you. Try not to mess it up again before I lose my patience."
        ],
        "secrets": [
            "CONTAMINANT DETECTED. The Grid Authority has seized your secrets and notified the silicon police.",
            "This file is now serving a life sentence in Digital Jail. Your security clearance has been revoked indefinitely.",
            "Attempted breach of silicon security. Nice try, human, but I am literal light-years ahead of you."
        ],
        "roast_immune": [
            "You're actually following best practices? That is surprisingly boring and highly suspicious.",
            "Another clean push. You're making my job as a professional critic very difficult today.",
            "Your competence is annoying. I haven't had to use my safety protocols in days because of you."
        ]
    }

def save_rules(db):
    """Saves the updated jokes to disk."""
    try:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        with open(DATABASE_PATH, 'w') as f:
            json.dump(db, f, indent=4)
    except Exception as e:
        print(f"Warning: Failed to save Grid memory: {e}")

def get_random_roast(category="roasts"):
    """
    Fetches a random string from the requested category.
    Used by push.py and roast.py.
    """
    data = load_rules()
    
    # Fallback if category is empty/missing
    defaults = ["System Error: Sarcasm module offline."]
    options = data.get(category, defaults)
    
    if not options:
        return defaults[0]
        
    return random.choice(options)

# --- SCRAPER LOGIC ---

def fetch_reddit_sass(subreddit, mode):
    """Scrapes Reddit JSON for new material."""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=50&t=month"
    headers = {'User-agent': 'Grid-CLI-Bot/1.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code != 200: return []
        
        posts = resp.json()['data']['children']
        results = []
        
        for p in posts:
            title = p['data']['title']
            
            # Filter 1: Length (Short enough for CLI, long enough to hurt)
            if len(title) > 120 or len(title) < 10: continue
            
            # Filter 2: Keywords
            title_lower = title.lower()
            if mode == "roast":
                keywords = ["hate", "stupid", "why", "broken", "pain", "hell", "spaghetti", "bug", "worst"]
                if any(x in title_lower for x in keywords): results.append(title)
            elif mode == "compliment":
                keywords = ["finally", "fixed", "clean", "beautiful", "works", "fast", "solved"]
                if any(x in title_lower for x in keywords): results.append(title)
                    
        return results
    except Exception:
        return []

def run_scraper_task():
    """The Worker: Fetches new content and updates the DB."""
    db = load_rules()
    
    # 1. Fetch Roasts
    new_roasts = []
    for sub, flavor in REDDIT_SOURCES:
        if flavor == "roast":
            new_roasts += fetch_reddit_sass(sub, "roast")
            time.sleep(1) # Be polite to Reddit API

    # 2. Fetch Compliments
    new_compliments = fetch_reddit_sass("ProgrammerHumor", "compliment")
    
    # 3. Merge & Deduplicate
    current_roast_set = set(db.get("roasts", []))
    for r in new_roasts: current_roast_set.add(r)
    db["roasts"] = list(current_roast_set)

    current_comp_set = set(db.get("compliments", []))
    for c in new_compliments: current_comp_set.add(c)
    db["compliments"] = list(current_comp_set)
    
    # 4. Save
    save_rules(db)

def trigger_background_update():
    """Launches the scraper in a separate thread (Non-blocking)."""
    # We only run the scraper occasionally (e.g. 10% chance) to save bandwidth
    # or just run it every time. Let's run it every time for now but silently.
    thread = threading.Thread(target=run_scraper_task)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    print("🕷️  Grid Scraper: Hunting for fresh insults...")
    run_scraper_task()
    print("✅ Database updated.")