import requests
import json
import os
import random
import time
from grid.core import utils

# --- CONFIGURATION ---
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../data/rules.json")

REDDIT_SOURCES = [
    ("ProgrammerHumor", "roast"), 
    ("badcode", "roast"), 
    ("programminghorror", "roast"),
    ("ProgrammerHumor", "compliment") 
]

def load_db():
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
        ]
    }

def save_db(db):
    """Saves the updated jokes to disk."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with open(DATABASE_PATH, 'w') as f:
        json.dump(db, f, indent=4)

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
            
            # Filter 1: Length
            if len(title) > 120 or len(title) < 10: continue
            
            # Filter 2: Keywords
            title_lower = title.lower()
            if mode == "roast":
                keywords = ["hate", "stupid", "why", "broken", "pain", "hell", "spaghetti", "bug"]
                if any(x in title_lower for x in keywords): results.append(title)
            elif mode == "compliment":
                keywords = ["finally", "fixed", "clean", "beautiful", "works", "fast"]
                if any(x in title_lower for x in keywords): results.append(title)
                    
        return results
    except Exception:
        return []

def update_wit():
    """Background Task: Updates the database with new content."""
    db = load_db()
    
    # 1. Fetch Roasts
    new_roasts = []
    for sub, flavor in REDDIT_SOURCES:
        if flavor == "roast":
            new_roasts += fetch_reddit_sass(sub, "roast")
            time.sleep(0.5) 

    # 2. Fetch Compliments
    new_compliments = fetch_reddit_sass("ProgrammerHumor", "compliment")
    
    # 3. Merge & Deduplicate
    current_roast_set = set(db["roasts"])
    for r in new_roasts: current_roast_set.add(r)
    db["roasts"] = list(current_roast_set)

    current_comp_set = set(db["compliments"])
    for c in new_compliments: current_comp_set.add(c)
    db["compliments"] = list(current_comp_set)
    
    # 4. Save
    save_db(db)

if __name__ == "__main__":
    print("🕷️  Grid Scraper: Hunting for fresh insults...")
    update_wit()
    print("✅ Database updated.")