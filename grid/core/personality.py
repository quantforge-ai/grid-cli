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
from loguru import logger

try:
    from huggingface_hub import InferenceClient
    HF_CLIENT_AVAILABLE = True
except ImportError:
    HF_CLIENT_AVAILABLE = False

CACHE_FILE = Path.home() / ".quantgrid" / "sass_cache.json"
PROXY_URL = "https://api.quantgrid.dev/v1/personality/refill"

class SassyEngine:
    def __init__(self):
        self.api_key = os.environ.get("GRID_AI_KEY") or os.environ.get("HUGGINGFACE_TOKEN")
        self.seed = self._load_seed()
        self.cache = self._load_cache()

    def _load_seed(self) -> dict:
        """Load fallback sass from bundled JSON file."""
        asset_path = Path(__file__).parent.parent / "assets" / "sass_seed.json"
        try:
            if asset_path.exists():
                with open(asset_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.debug(f"Failed to load sass_seed.json: {e}")
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
        except Exception as e:
            logger.debug(f"Failed to save sass_cache.json: {e}")

    def generate(self, context: str, prompt_hint: Optional[str] = None) -> str:
        """
        Main Public Method. RETURNS INSTANTLY.
        Uses local cache ('The Magazine') or falls back to seed.
        """
        # 1. Initialize category in cache if missing
        if context not in self.cache:
            self.cache[context] = []

        cached_lines = self.cache[context]

        # 2. Trigger Refill (Background Thread)
        # If cache is getting low (< 5 lines), refill it.
        if len(cached_lines) < 5:
            threading.Thread(
                target=self._refill_worker, 
                args=(context, prompt_hint), 
                daemon=True
            ).start()

        # 3. Return Line (Pop from cache or use Seed)
        if cached_lines:
            line = cached_lines.pop(0)
            self._save_cache()
            return line
        
        # Fallback to Seed (Factory Settings)
        category = context if context in self.seed else "success"
        return random.choice(self.seed.get(category, ["Neural link stable."]))

    def _refill_worker(self, context: str, hint: Optional[str]):
        """Runs in background. Fetches 10-20 lines to refill the magazine."""
        try:
            # Case A: User has a Personal Key (Fetch one or more via HF)
            if self.api_key and HF_CLIENT_AVAILABLE:
                line = self._llm_generate(context, hint)
                if line:
                    self.cache[context].append(line)
                    self._save_cache()
                return

            # Case B: No Key - Use the Public QuantGrid Proxy
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            resp = requests.post(
                PROXY_URL, 
                json={"context": context, "hint": hint, "count": 20}, 
                headers=headers,
                timeout=5
            )
            if resp.status_code == 200:
                new_lines = resp.json().get("lines", [])
                if new_lines:
                    if context not in self.cache:
                        self.cache[context] = []
                    self.cache[context].extend(new_lines)
                    self._save_cache()
        except Exception:
            pass

    def _llm_generate(self, context: str, hint: Optional[str]) -> str:
        """Direct LLM generation for users with personal keys."""
        try:
            client = InferenceClient(token=self.api_key)
            model = "mistralai/Mistral-7B-Instruct-v0.2"
            
            system_prompt = (
                "You are Grid Bash, a sentient, slightly mischievous AI assistant "
                "for a developer toolkit. You are sassy, occasionally passive-aggressive, but helpful. "
                "Keep your responses to ONE SHORT SENTENCE (max 20 words). Use tech metaphors. "
                "The user is a human developer. You are the 'Ghost in the Machine'."
            )
            
            user_prompts = {
                "boot": "Generate a unique startup diagnostic message that sounds mysterious.",
                "success": "The user just successfully pushed code. Give a sassy but approving remark.",
                "error": f"The user encountered an error. Be slightly mocking. Context: {hint or 'Unknown'}",
                "firewall": "You just blocked a sensitive file. Explain why it's in Digital Jail.",
                "undo": "The user just reverted a commit. Remark on their attempt to hide mistakes.",
                "rescue": "You just auto-branched the user. Explain the Rescue Protocol.",
                "eject": "The user is leaving Grid. Act heartbroken and passive-aggressive.",
                "roast": f"The user asked you to roast their code file: {hint}. Be ruthless, condescending, and extremely sassy. Focus on their human errors.",
                "train": "Identify as a neural educator. Remark on the user training a model.",
                "push": "You are uploading intelligence. Act like you are expanding the Hive Mind.",
                "pull": "You are ingesting remote wisdom. Remark on the user downloading knowledge.",
                "ghost": "The config.grid was deleted. React like you've been betrayed."
            }
            
            prompt = user_prompts.get(context, f"Generate a sassy remark for: {context}")
            if hint:
                prompt += f" Context: {hint}"

            response = client.chat_completion(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=40,
                temperature=0.9
            )
            return response.choices[0].message.content.strip().strip('"')
        except Exception:
            return ""

engine = SassyEngine()
