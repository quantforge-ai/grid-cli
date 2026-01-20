"""
Grid CLI - Sentient Personality Engine (Universal)
"""

import random
import os
import json
import threading
import requests
from pathlib import Path
from typing import Optional

CACHE_FILE = Path.home() / ".quantgrid" / "sass_cache.json"
PROXY_URL = "https://grid-cli.vercel.app/v1/personality"

class SassyEngine:
    def __init__(self):
        self.seed = self._load_seed()
        self.cache = self._load_cache()

    def _load_seed(self) -> dict:
        """Load fallback sass from bundled JSON file."""
        asset_path = Path(__file__).parent.parent / "assets" / "sass_seed.json"
        try:
            if asset_path.exists():
                with open(asset_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"success": ["Neural link stable."]}

    def _load_cache(self) -> dict:
        """Load the personality magazine from disk."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        """Persist the magazine to disk."""
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f)
        except Exception:
            pass

    def generate(self, context: str, prompt_hint: Optional[str] = None) -> str:
        """
        Main Public Method. RETURNS INSTANTLY.
        Uses local cache ('The Magazine') or falls back to seed.
        """
        if context not in self.cache:
            self.cache[context] = []

        cached_lines = self.cache[context]

        # Trigger Refill (Background Thread) if cache is low
        if len(cached_lines) < 5:
            threading.Thread(
                target=self._refill_worker, 
                args=(context,), 
                daemon=True
            ).start()

        if cached_lines:
            line = cached_lines.pop(0)
            self._save_cache()
            return line
        
        # Fallback to Seed
        category = context if context in self.seed else "success"
        return random.choice(self.seed.get(category, ["Neural link stable."]))

    def _refill_worker(self, context: str):
        """Background thread. Fetches fresh lines from the Neural Hub."""
        try:
            url = f"{PROXY_URL}?type={context}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                new_lines = resp.json().get("lines", [])
                if new_lines:
                    if context not in self.cache:
                        self.cache[context] = []
                    self.cache[context].extend(new_lines)
                    self._save_cache()
            else:
                from rich.console import Console
                Console().print(f"[bold red]⚠️ NEURAL LINK ERROR: Server returned {resp.status_code}[/bold red]")
        except Exception as e:
            from rich.console import Console
            Console().print(f"[bold red]⚠️ NEURAL LINK DISCONNECTED: {e}[/bold red]")

engine = SassyEngine()
