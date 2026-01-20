from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import random

app = Flask(__name__)
CORS(app)

# Vercel Environment Variables
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = os.environ.get("HF_API_URL", "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2")

ROAST_PROMPT = """
You are a cynical, elite senior software engineer. 
Analyze the following code. Find one specific flaw. 
Insult the user's intelligence based on that flaw. 
Be short (under 20 words), witty, and brutal.
"""

@app.route('/v1/health', methods=['GET'])
def health():
    return jsonify({"status": "neural_link_active", "version": "1.0.0"})

@app.route('/v1/personality', methods=['GET'])
def get_personality():
    category = request.args.get('type', 'neutral')
    lines = [
        "I've seen cleaner code in a spaghetti factory.",
        "Oh look, another commit. How exciting.",
        "My neural pathways hurt just looking at this.",
        "Are we deploying bugs today? Excellent.",
        "Optimizing for job security, I see."
    ]
    random.shuffle(lines)
    return jsonify({"lines": lines})

@app.route('/v1/roast', methods=['POST'])
def roast():
    data = request.json
    code_snippet = data.get('code', '')

    if not HF_TOKEN:
        return jsonify({"error": "Brain Lobotomized (Missing HF_TOKEN)"}), 500

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"<s>[INST] {ROAST_PROMPT} \n\n Code: {code_snippet} [/INST]",
        "parameters": {"max_new_tokens": 60, "temperature": 0.8, "return_full_text": False}
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Vercel
app = app
