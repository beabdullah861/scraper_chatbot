# ScriptForge — AI YouTube Shorts Script Writer

An AI-powered chatbot that generates YouTube Shorts scripts using OpenRouter API. Built with Python Flask backend and HTML/CSS/JS frontend.

---

## Project Structure

```
Final AI Project/
│
├── app.py           # Flask backend — handles API calls to OpenRouter
├── index.html       # Frontend — chatbot UI
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## Features

- **Horror Stories** — Creepy, atmospheric 60-second Shorts scripts
- **Educational Scripts** — Fast, one-concept educational Shorts
- **Viral Shorts** — High-energy, shareable Shorts scripts
- **Hooks & Titles** — 3 hook and title options per topic
- **SEO Descriptions** — Hashtags, tags, and keyword-rich descriptions
- Token usage tracker shown after every generation
- Copy script button on every response
- Works with any free model on OpenRouter

---

## Requirements

- Python 3.8 or above
- OpenRouter account and API key (free — no credit card needed)
- VS Code (recommended)
- Internet connection

---

## Installation

**Step 1 — Clone or download the project folder**

Place all files in one folder, for example:
```
C:\Users\YourName\Desktop\Final AI Project\
```

**Step 2 — Open the folder in VS Code**

**Step 3 — Install Python dependencies**

Open terminal in VS Code (`Ctrl + ~`) and run:
```bash
pip install -r requirements.txt
```

---

## Getting Your OpenRouter API Key

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Go to **Keys** from the top menu
4. Click **Create Key**
5. Copy the key (starts with `sk-or-v1-...`)

No credit card required for free models.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Cannot connect to backend" | Make sure `python app.py` is running in terminal |
| 404 on `127.0.0.1:5000` | That is normal — open `127.0.0.1:8080` instead |
| "No endpoint for model" | Model changed — `openrouter/auto` is set by default and handles this |
| Script not generating | Check your API key is correct and has no extra spaces |
| Blank page on `8080` | Make sure terminal 2 is `cd` into the correct project folder |

---

## Tech Stack

| Part | Technology |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| AI API | OpenRouter (`openrouter/auto`) |
| Model | Auto-selected free model |

---

## Token Limits Per Category

| Category | Max Tokens |
|---|---|
| Horror Stories | 600 |
| Educational | 600 |
| Viral Shorts | 500 |
| Hooks & Titles | 300 |
| SEO Description | 250 |

---

## Notes

- All scripts are written for **60-second vertical Shorts only**
- The model `openrouter/auto` automatically picks the best available free model
- Free tier on OpenRouter allows 50 requests per day
- Keep both terminals open while using the app

---

## Developer

Built with Flask + Vanilla JS + OpenRouter API.
