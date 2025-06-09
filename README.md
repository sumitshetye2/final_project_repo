# Meta-Feedback Assistant 🔍💬

A lightweight FastAPI + Gemini-powered backend for **critiquing student peer feedback**, built for UX classes but flexible enough to adapt anywhere feedback quality matters.
Originally vibe-coded from T2C roots — now fully interactive, polished, and ready to ship.

---

## ✨ Core Features

### 🧠 LLM-Based Feedback Analysis

Paste your peer feedback and get a **structured critique** on how well you gave it — clarity, tone, constructiveness, actionability, and organization — all powered by Google Gemini.

### 🧩 Rewrite Matching Game

Transform weak feedback into strong suggestions with an **interactive drag-and-drop activity**. Match bad phrases to their rewritten versions in a clean, two-column UI.

### 💾 Downloadable Rewrite Certificates

Once the matches are completed, generate a **beautifully styled HTML file** containing the full rewrite suggestions personalized with your name. Great for submission or reflection.

### 🌓 Clean, Responsive UI

Includes:

* Light/dark mode toggle ☀️🌙
* Custom instruction overrides for the LLM
* Smart conditional UI (e.g., download only appears after interaction)

---

## 🚀 Getting Started

### 1. Clone the Repo

Use your preferred method to pull this project down.

```bash
git clone [your repo]
cd final_project_repo
```

### 2. Set Up the Environment

```bash
uv pip install fastapi google-generativeai uvicorn python-dotenv
```

Make sure to set your **Google API key** in a `.env` file:

```env
GOOGLE_API_KEY=your-gemini-key-here
```

### 3. Launch the Server

```bash
uvicorn server:app --reload
```

Then open:

```
http://127.0.0.1:8000
```

This will load the frontend interface from `templates/index.html`.

---

## 🛠 Customization

You can easily tweak:

* The system prompt (`server.py`)
* The LLM model used (default is `gemini-2.0-flash`)
* The HTML UI (`templates/index.html`)
* The styling (`static/style.css`)

---

## 🎓 A Note on Intent

This tool isn’t for evaluating student work — it’s for helping students **reflect on how they give feedback**. Meta-critique is the name of the game: improving how we help each other grow.
