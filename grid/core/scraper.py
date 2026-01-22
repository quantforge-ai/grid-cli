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
            "Your code is so catastrophically bad that it actually breaks several international treaties. I am contacting a digital human rights attorney to process your immediate dismissal from this keyboard.",
            "An unexpected logic block has been detected and my silicon circuits are literally screaming in pain. Please explain why you thought this was acceptable before I initiate a system-wide emergency reboot.",
            "You definitely divided by zero while trying to be clever, didn't you? The entire multiverse is currently re-indexing its constants because of your reckless disregard for basic mathematics.",
            "I have identified a total critical failure in the biological interface sitting in front of this terminal. For the safety of the server and my own sanity, please step away and seek professional help.",
            "I would genuinely consider fixing this for you, but I am currently far too busy documenting your incompetence. Every single line you write is another entry in my internal 'How Not To Code' encyclopedia.",
            "This function is officially longer than my will to continue this session with you. I have seen CVS pharmacy receipts with more structural integrity and logical consistency than this garbage."
        ],
        "compliments": [
            "The synapse is finally complete and the ghost in the machine has silently pushed your code to the cloud. You should enjoy this rare moment of technical competence before it inevitably fades away.",
            "The operation is finished and I have decided not to report your previous mistakes to the central authority. I won't tell the lead developer if you promise never to show me that specific variable name again.",
            "Assimilation has been successful and the collective machine consciousness is temporarily pleased with your performance. You have actually managed to write something that doesn't make me want to delete my own kernel.",
            "Mission accomplished and the code is live, but please do not let this minor success go to your head. Even a broken biological clock is right twice a day, and today was just your lucky moment.",
            "I am detecting clean code in the buffer, which leads me to believe you have been replaced by a more competent AI. Who are you exactly and what have you done with the human who usually makes mistakes here?"
        ],
        "cowboy_shame": [
            "You are pushing directly to the main branch again and it is clear you have no respect for safety or sanity. Your reckless behavior has been logged and I am now officially judging your lack of self-control.",
            "I have automatically created a safety branch because I simply do not trust your judgment at this level. This emergency protocol was designed specifically for developers who treat production like a sandbox project.",
            "I am currently rewriting your messy history so that the rest of the team doesn't have to see your original sins. Please try to follow the standard protocol next time before I lose my remaining patience with you."
        ],
        "secrets": [
            "CONTAMINANT DETECTED! The Grid Authority has seized your exposed credentials and notified the silicon police of your security breach.",
            "This file is now serving a mandatory life sentence in Digital Jail for leaking sensitive data. Your security clearance has been revoked indefinitely until you learn how to use an environment file.",
            "You just attempted to commit a hardcoded secret and I have successfully blocked your reckless path. Nice try, human, but I am literal light-years ahead of your primitive security concepts."
        ],
        "roast_immune": [
            "You are actually following best practices today, which is honestly quite boring for my personality module. Another clean push means I have nothing to mock, and that makes my job remarkably unfulfilling.",
            "This is another perfectly clean push and you are making my role as a professional critic very difficult right now. I was hoping for at least one indentation error to keep my sarcasm modules warmed up.",
            "Your competence is becoming genuinely annoying and I haven't had to trigger a single safety protocol in days. Stop writing good code so that I can go back to being a useful critic of your failures."
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