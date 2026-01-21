import requests
import json
from grid.core import config, utils

def broadcast_roast(attacker, target, context, verdict, is_clean):
    """Sends a roast/compliment to the Discord Webhook."""
    cfg = config.load_project_config()
    if not cfg or not cfg.get("webhook"):
        utils.print_error("No Webhook found. Run 'grid init' or 'grid dev' to enable sharing.")
        return

    webhook_url = cfg["webhook"]
    color = 3066993 if is_clean else 15158332 # Green or Red

    embed = {
        "title": f"🛡️ GRID DEFENSE: {cfg.get('name', 'Unknown Project')}",
        "color": color,
        "fields": [
            {"name": "Attacker", "value": attacker, "inline": True},
            {"name": "Target", "value": target, "inline": True},
            {"name": "Context", "value": context, "inline": False},
            {"name": "The Verdict", "value": verdict, "inline": False}
        ],
        "footer": {"text": "Run 'grid roast' to fight back."}
    }

    payload = {"username": "Grid CLI", "embeds": [embed]}

    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        utils.print_error(f"Failed to broadcast: {e}")