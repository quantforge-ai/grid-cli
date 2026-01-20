from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
from huggingface_hub import InferenceClient

app = Flask(__name__)
CORS(app)

# 1. Setup the Official Client
# It automatically handles the URL routing and authentication headers.
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(token=HF_TOKEN)

@app.route('/v1/health', methods=['GET'])
def health():
    return jsonify({
        "status": "neural_link_active", 
        "version": "1.0.0",
        "engine": "huggingface_hub.InferenceClient"
    })

@app.route('/v1/personality', methods=['GET'])
def get_personality():
    category = request.args.get('type', 'neutral')
    
    # NICE GREETINGS (For Boot)
    if category == "boot":
        lines = [
            "Neural Link Established. Systems Green.",
            "Welcome back, User. The Grid is waiting.",
            "Personality Core: Online. Sarcasm: 100%.",
            "Hardware detected. Assimilation complete.",
            "Grid Terminal v1.0 ready for input."
        ]
    # MEAN INSULTS (For Roast)
    elif category == "roast":
        lines = [
            "I've seen cleaner code in a spaghetti factory.",
            "My neural pathways hurt just looking at this.",
            "Are we deploying bugs today? Excellent.",
            "Delete this before anyone sees it.",
            "Optimizing for job security, I see."
        ]
    # NEUTRAL (For idle)
    else: 
        lines = ["Waiting for command...", "Processing...", "I'm bored.", "System stable."]

    random.shuffle(lines)
    return jsonify({"lines": lines})

@app.route('/v1/roast', methods=['POST'])
def roast():
    data = request.json
    code_snippet = data.get('code', '')

    if not HF_TOKEN:
        return jsonify({"error": "Brain Lobotomized (Missing HF_TOKEN)"}), 500

    try:
        # The PROMPT optimized for the official client
        prompt = f"""<|system|>
You are a cynical senior software engineer. 
Analyze the user's code. Find one specific flaw. 
Insult the user's intelligence based on that flaw. 
Be short, witty, and brutal.</s>
<|user|>
Code:
{code_snippet}</s>
<|assistant|>"""

        # The Official Call (No manual URLs or headers needed)
        response = client.text_generation(
            prompt,
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=100,
            temperature=0.8,
            stop_sequences=["</s>"]
        )
        
        # Clean up the response (remove the prompt if it leaks, though client usually doesn't)
        roast_text = response.strip()
        
        # Return in the format the CLI expects (List of dicts)
        return jsonify([{"generated_text": roast_text}])

    except Exception as e:
        # Error diagnostics are automatically better with the library
        return jsonify({"error": f"HF Client Error: {str(e)}"}), 500

# Required for Vercel
app = app
