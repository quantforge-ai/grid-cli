import requests
import json
import os
import random
import time
from grid.core import utils

# --- CONFIGURATION ---
# We store the DB relative to this file's location
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../data/rules.json")

# Sources and their "flavor"
REDDIT_SOURCES = [
    ("ProgrammerHumor", "roast"), 
    ("badcode", "roast"), 
    ("programminghorror", "roast"),
    ("ProgrammerHumor", "compliment") # We specific filters for good vibes
]

def load_db():
    """Loads the rules.json file or creates a default one."""
    if os.path.exists(DATABASE_PATH):
        try:
            with open(DATABASE_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass # File corrupted, reset it
            
    # Default Starting Database (The Seed)
    return {
        "roasts": [
            "Your code is so bad it breaks the Geneva Convention.",
            "I've seen cleaner code in a spaghetti factory.",
            "This function is longer than my will to live."
        ],
        "compliments": [
            "This code is... acceptable. I'm suspicious.",
            "Finally, some logic. Don't get used to this praise.",
            "Clean code? Who are you and what did you do with the user?"
        ],
        "cowboy_shame": [
            "Pushing to main? You have a death wish.",
            "I created a safety branch because I don't trust you."
        ],
        "secrets": [
            "Leaking secrets? I'll tweet this if you do it again.",
            "Nice API key. Would be a shame if someone stole it."
        ]
    }

def save_db(db):
    """Saves the updated jokes to disk."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with open(DATABASE_PATH, 'w') as f:
        json.dump(db, f, indent=4)

def fetch_reddit_sass(subreddit, mode):
    """
    Scrapes Reddit JSON (No API Key needed for read-only).
    mode='roast': Looks for pain words.
    mode='compliment': Looks for success words.
    """
    # specific 'top' endpoint to get the best content
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit=50&t=month"
    headers = {'User-agent': 'Grid-CLI-Bot/1.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=4)
        if resp.status_code != 200: 
            return []
        
        posts = resp.json()['data']['children']
        results = []
        
        for p in posts:
            title = p['data']['title']
            
            # FILTER 1: Length (Short punchlines only)
            if len(title) > 120 or len(title) < 10:
                continue
            
            # FILTER 2: Keyword Targeting
            title_lower = title.lower()
            
            if mode == "roast":
                # We want the suffering
                keywords = ["hate", "stupid", "why", "broken", "pain", "hell", "spaghetti", "bug"]
                if any(x in title_lower for x in keywords):
                    results.append(title)
                    
            elif mode == "compliment":
                # We want the rare wins
                keywords = ["finally", "fixed", "clean", "beautiful", "works", "fast"]
                if any(x in title_lower for x in keywords):
                    results.append(title)
                    
        return results
    except Exception:
        # Silently fail if internet is down (don't annoy user)
        return []

def update_wit():
    """
    The Main Engine. Updates the database with new content.
    """
    # Note: We do NOT print here because this usually runs in a background thread.
    # We only log to the file.
    
    db = load_db()
    
    # 1. Fetch Roasts
    new_roasts = []
    for sub, flavor in REDDIT_SOURCES:
        if flavor == "roast":
            new_roasts += fetch_reddit_sass(sub, "roast")
            time.sleep(0.5) # Be nice to Reddit's API rate limits

    # 2. Fetch Compliments (Rare)
    new_compliments = fetch_reddit_sass("ProgrammerHumor", "compliment")
    
    # 3. Merge & Deduplicate
    initial_roast_count = len(db["roasts"])
    
    # Add new ones only if unique
    current_roast_set = set(db["roasts"])
    for r in new_roasts:
        current_roast_set.add(r)
    db["roasts"] = list(current_roast_set)

    current_comp_set = set(db["compliments"])
    for c in new_compliments:
        current_comp_set.add(c)
    db["compliments"] = list(current_comp_set)
    
    # 4. Save
    save_db(db)
    
    # Optional: Logic to rotate old jokes out if the file gets too big ( > 500 lines) can go here.

if __name__ == "__main__":
    # Manual test run
    print("🕷️  Grid Scraper: Hunting for fresh insults...")
    update_wit()
    print("✅ Database updated.")