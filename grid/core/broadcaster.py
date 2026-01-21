import requests
import json
from grid.core import config, utils

def broadcast_roast(attacker, victim, verdict, flavor, is_compliment):
    """
    Sends the roast to the team channel via Webhook.
    """
    cfg = config.load_config()
    if not cfg or not cfg.get("webhook"):
        utils.print_error("Link failure: No Webhook URL found. Run 'grid init' to set up team chat.")
        return

    webhook_url = cfg["webhook"]
    project = cfg.get("project", "Unknown Project")
    
    # --- FORMATTING THE MESSAGE ---
    # We use a generic format that works decently on Slack & Discord
    
    color = 0x00FF00 if is_compliment else 0xFF0000 # Green vs Red
    title = f"🛡️ GRID DEFENSE: {project}" if is_compliment else f"🔥 GRID ALERT: {project}"
    
    # The Payload (Discord Style Embeds - usually works on Slack too with adapters)
    payload = {
        "username": "Grid CLI",
        "avatar_url": "https://i.imgur.com/4M34hi2.png", # Generic Robot Icon
        "embeds": [{
            "title": title,
            "color": color,
            "fields": [
                {"name": "Attacker", "value": attacker, "inline": True},
                {"name": "Target", "value": victim, "inline": True},
                {"name": "Analysis", "value": verdict, "inline": False},
                {"name": "The Verdict", "value": flavor, "inline": False}
            ],
            "footer": {"text": "Run 'grid roast' to fight back."}
        }]
    }

    # For Slack, the payload structure is different, but let's stick to a simple JSON post first.
    # If the user provided a raw Slack webhook, we might need a simpler text fallback.
    if "hooks.slack.com" in webhook_url:
        # Slack Simple Fallback
        slack_text = f"*{title}*\n*Target:* {victim}\n*Analysis:* {verdict}\n> {flavor}"
        payload = {"text": slack_text}

    try:
        requests.post(webhook_url, json=payload)
        utils.print_success("Roast uploaded to Team Channel.")
    except Exception as e:
        utils.print_error(f"Transmission failed: {e}")