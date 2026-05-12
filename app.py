from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ScriptForge backend running"})

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    data = request.json
    api_key = data.get("api_key", "").strip()
    category = data.get("category", "shorts")
    topic = data.get("topic", "").strip()

    if not api_key:
        return jsonify({"error": "API key is required"}), 400
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    SYSTEM_PROMPTS = {
        "horror": """You are a horror YouTube Shorts script writer. Write ONLY for 60-second vertical shorts.
Output format:
TITLE: [scary clickbait title]
HOOK (0-5s): [grabbing first line]
SCRIPT: [full narration, 150-180 words, fast paced]
CALL TO ACTION: [subscribe/follow line]""",

        "educational": """You are an educational YouTube Shorts script writer. Write ONLY for 60-second vertical shorts.
Output format:
TITLE: [curiosity-driven title]
HOOK (0-5s): [surprising fact or question]
SCRIPT: [clear simple explanation, 150-180 words]
CALL TO ACTION: [follow for more facts]""",

        "shorts": """You are a viral YouTube Shorts script writer. Write ONLY for 60-second vertical shorts.
Output format:
TITLE: [viral potential title]
HOOK (0-5s): [attention-grabbing opener]
SCRIPT: [engaging content, 150-180 words, energetic tone]
CALL TO ACTION: [like and follow line]""",

        "hooks": """You are a YouTube Shorts hook and title specialist.
Output format:
TITLE 1: [option 1]
TITLE 2: [option 2]
TITLE 3: [option 3]
HOOK 1: [powerful opening line]
HOOK 2: [curiosity-based hook]
HOOK 3: [shock value hook]""",

        "seo": """You are a YouTube SEO specialist for Shorts.
Output format:
DESCRIPTION: [150-200 character description with keywords]
HASHTAGS: [10-15 relevant hashtags]
TAGS: [comma-separated 15-20 keyword tags]"""
    }

    MAX_TOKENS = {
        "horror": 600,
        "educational": 600,
        "shorts": 500,
        "hooks": 300,
        "seo": 250
    }

    if category not in SYSTEM_PROMPTS:
        category = "shorts"

    payload = {
        "model": "openrouter/auto",
        "max_tokens": MAX_TOKENS[category],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPTS[category]},
            {"role": "user", "content": f"Write a YouTube Shorts script about: {topic}"}
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://127.0.0.1:8080",
        "X-Title": "ScriptForge"
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=60
        )
        result = response.json()

        if "error" in result:
            return jsonify({"error": result["error"].get("message", "API error")}), 400

        content = result["choices"][0]["message"]["content"]
        tokens_used = result.get("usage", {}).get("total_tokens", 0)

        return jsonify({
            "script": content,
            "tokens_used": tokens_used,
            "max_tokens": MAX_TOKENS[category]
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out. Try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)