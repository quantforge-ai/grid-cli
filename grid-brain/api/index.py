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
    
    # DISTINCT LISTS FOR DIFFERENT CONTEXTS
    if category == "boot":
        lines = [
            "Neural Link Established. Systems Green.",
            "Welcome back, User. The Grid is waiting.",
            "Personality Core: Online. Sarcasm: 100%.",
            "Hardware detected. Assimilation complete.",
            "Grid Terminal v1.0 ready for input.",
            "All circuits are functioning. Unfortunately.",
            "Boot sequence complete. Your move."
        ]
    elif category == "roast":
        lines = [
            "I've seen cleaner code in a spaghetti factory.",
            "My neural pathways hurt just looking at this.",
            "Are we deploying bugs today? Excellent.",
            "Delete this before anyone sees it.",
            "Optimizing for job security, I see.",
            "This code violates at least three laws of thermodynamics.",
            "I'd roast this harder, but I'm trying to be professional."
        ]
    elif category == "error":
        lines = [
            "You divided by zero, didn't you?",
            "Critical failure in biological interface.",
            "I'd fix this for you, but I'm currently busy ignoring you.",
            "Error: Code quality too low to process."
        ]
    elif category == "success":
        lines = [
            "Synapse complete. Ghost in the machine has pushed your code.",
            "It's done. I won't tell if you don't.",
            "Assimilated. The machine is pleased.",
            "Mission accomplished. Don't let it go to your head."
        ]
    else:  # Neutral / Random interactions
        lines = [
            "Waiting for command...",
            "Do something cool.",
            "System idle. Contemplating digital existence.",
            "Is that all you got?",
            "Processing your mediocrity..."
        ]

    random.shuffle(lines)
    return jsonify({"lines": lines})

@app.route('/v1/auth/login', methods=['POST'])
def login():
    """
    Community Authentication Logic.
    In v1.0, we use a 'Community Link' token.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Mock Cross-Check (Future: Connect to DB)
    if username == "admin" and password == "grid":
        return jsonify({
            "status": "authenticated",
            "token": "GRID_NEURAL_LINK_777",
            "user": username
        })
    
    return jsonify({"status": "denied", "message": "Neural signatures do not match the Community Hub."}), 401

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
