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
            "Your code is so bad it breaks the Geneva Convention.",
            "Unexpected logic block. My circuits hurt.",
            "You divided by zero, didn't you?",
            "Critical failure in biological interface.",
            "I'd fix this for you, but I'm currently busy ignoring you.",
            "This function is longer than my will to live."
        ],
        "compliments": [
            "Synapse complete. Ghost in the machine has pushed your code.",
            "It's done. I won't tell if you don't.",
            "Assimilated. The machine is pleased.",
            "Mission accomplished. Don't let it go to your head.",
            "Clean code? Who are you and what did you do with the user?"
        ],
        "cowboy_shame": [
            "Pushing to main? You have a death wish.",
            "I created a safety branch because I don't trust you.",
            "Rewriting history for you. Try not to mess it up again."
        ],
        "secrets": [
            "CONTAMINANT DETECTED. The Grid Authority has seized your secrets.",
            "This file is now serving a life sentence in Digital Jail.",
            "Attempted breach of silicon security. Nice try, human."
        ],
        "roast_immune": [
            "You're actually following best practices? Boring.",
            "Another clean push. You're making my job as a critic very difficult.",
            "Your competence is annoying. I haven't had to use my safety protocols in days."
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