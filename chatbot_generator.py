"""
Chatbot Generator Module (FIXED FOR PRODUCTION / RENDER SAFE)

Fixes:
- No broken f-string JS braces
- Safe HTML + JS injection
- Clean structure for deployment
"""

import json
import os
import re
from datetime import datetime
import requests


GENERATED_DIR = os.path.join(os.path.dirname(__file__), "generated_chatbots")


class ChatbotGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"

    # ---------------------------
    # MAIN GENERATE FUNCTION
    # ---------------------------
    def generate(self, scraped_data: dict, chatbot_id: str, source_url: str) -> dict:
        chatbot_dir = os.path.join(GENERATED_DIR, chatbot_id)
        os.makedirs(chatbot_dir, exist_ok=True)

        system_prompt = self._build_system_prompt(scraped_data)
        brand = self._extract_brand(scraped_data)

        knowledge = {
            "chatbot_id": chatbot_id,
            "source_url": source_url,
            "brand": brand,
            "system_prompt": system_prompt,
            "api_key": self.api_key,
            "created_at": datetime.now().isoformat(),
            "scraped_data_summary": {
                "title": scraped_data.get("title", ""),
                "services": scraped_data.get("services", [])[:10],
                "products": scraped_data.get("products", [])[:10],
                "contact": scraped_data.get("contact", {}),
                "about": scraped_data.get("about", "")[:500],
                "location": scraped_data.get("location", ""),
            }
        }

        with open(os.path.join(chatbot_dir, "knowledge.json"), "w", encoding="utf-8") as f:
            json.dump(knowledge, f, indent=2, ensure_ascii=False)

        with open(os.path.join(chatbot_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(self._generate_chatbot_html(brand, chatbot_id))

        with open(os.path.join(chatbot_dir, "widget.js"), "w", encoding="utf-8") as f:
            f.write(self._generate_widget_js(brand, chatbot_id))

        meta = {
            "chatbot_id": chatbot_id,
            "source_url": source_url,
            "title": brand["name"],
            "created_at": datetime.now().isoformat(),
            "pages_scraped": scraped_data.get("pages_scraped", 1),
        }

        with open(os.path.join(chatbot_dir, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return {
            "embed_code": self._generate_embed_code(chatbot_id),
            "brand": brand,
        }

    # ---------------------------
    # SYSTEM PROMPT
    # ---------------------------
    def _build_system_prompt(self, data: dict) -> str:
        summary = f"""
Website: {data.get('base_url', '')}
Business: {data.get('title', '')}
Services: {data.get('services', [])[:10]}
Products: {data.get('products', [])[:10]}
Contact: {data.get('contact', {})}
"""

        prompt = f"""
Create a customer support chatbot system prompt.

{summary}

Rules:
- Friendly and professional
- 2–4 sentences max
- Use provided business info only
- Say "I don't know" if info missing
"""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 800,
                },
                timeout=30
            )

            data_json = response.json()
            if "choices" in data_json:
                return data_json["choices"][0]["message"]["content"]

        except Exception as e:
            print("LLM failed:", e)

        return self._fallback_system_prompt(data)

    # ---------------------------
    # FALLBACK
    # ---------------------------
    def _fallback_system_prompt(self, data: dict) -> str:
        return f"You are a helpful assistant for {data.get('title', 'this business')}."

    # ---------------------------
    # BRAND EXTRACTION
    # ---------------------------
    def _extract_brand(self, data: dict) -> dict:
        title = data.get("title", "Business")
        name = re.sub(r'\s*[-|–].*$', '', title).strip()

        return {
            "name": name,
            "url": data.get("base_url", ""),
            "bot_name": f"{name.split()[0]} Assistant",
            "colors": {
                "primary": "#2563eb",
                "primary_dark": "#1d4ed8"
            }
        }

    # ---------------------------
    # HTML (FIXED JS ESCAPING)
    # ---------------------------
    def _generate_chatbot_html(self, brand: dict, chatbot_id: str) -> str:

        # JS stored as raw string (NO f-string injection issues)
        js_code = """
        function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            addMessage('user', text);
            input.value = '';

            fetch(`/chatbot/""" + chatbot_id + """/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            })
            .then(r => r.json())
            .then(data => addMessage('bot', data.reply))
            .catch(() => addMessage('bot', 'Error occurred'));
        }

        function addMessage(role, text) {
            const msg = document.createElement('div');
            msg.innerHTML = role + ': ' + text;
            document.getElementById('messages').appendChild(msg);
        }
        """

        return f"""
<!DOCTYPE html>
<html>
<head>
<title>{brand['name']}</title>
</head>
<body>

<div id="messages"></div>

<input id="userInput" />
<button onclick="sendMessage()">Send</button>

<script>
{js_code}
</script>

</body>
</html>
"""

    # ---------------------------
    # WIDGET JS (SAFE VERSION)
    # ---------------------------
    def _generate_widget_js(self, brand: dict, chatbot_id: str) -> str:

        return f"""
(function() {{

const CHATBOT_ID = "{chatbot_id}";
const API_BASE = "";

function toggleChat() {{
    alert("Chatbot {brand['name']} loaded!");
}}

window.ChatbotWidget = {{
    open: toggleChat
}};

}})();
"""

    # ---------------------------
    # EMBED CODE
    # ---------------------------
    def _generate_embed_code(self, chatbot_id: str) -> str:
        return f'<script src="/chatbot/{chatbot_id}/widget.js"></script>'