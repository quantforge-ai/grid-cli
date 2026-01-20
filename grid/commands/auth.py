import click
import os
import json

CONFIG_PATH = os.path.expanduser("~/.grid_config")

def save_key(key):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"api_key": key}, f)

def login():
    """Authenticate with the Neural Cloud."""
    click.echo(">> Authenticating with Grid Hive Mind...")
    key = click.prompt("Enter your API Key (Groq/Gemini)", hide_input=True)
    save_key(key)
    click.echo(">> Neural Link Established.")