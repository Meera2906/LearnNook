<div align="center">

# 📚 LearnNook

### Your Personal AI-Powered Study Corner

*An intelligent educational platform that transforms any topic into an immersive, interactive learning experience — powered by real-world photography and cutting-edge AI.*

[![Live Demo](https://img.shields.io/badge/🚀%20Launch%20App-learn--nook.vercel.app-8A2BE2?style=for-the-badge&logo=vercel&logoColor=white)](https://learn-nook.vercel.app)

[![Tech Stack](https://skillicons.dev/icons?i=fastapi,python,postgres,vercel&theme=dark)](https://skillicons.dev)

<p align="center">
  <img src="https://img.shields.io/badge/AI-OpenRouter-FF6B35?style=flat-square" />
  <img src="https://img.shields.io/badge/Database-Neon-00E5BF?style=flat-square" />
</p>

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
- [Deployment (Vercel + Neon)](#deployment-vercel--neon)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

**LearnNook** is a full-stack AI tutoring platform built to make self-directed learning feel effortless and engaging. At its core, the platform:

1. Takes a student's **grade, subject, and topic** as input.
2. Generates a **rich, pedagogically structured lesson** using a state-of-the-art LLM.
3. Sources a **real-world educational photograph** from Wikimedia Commons to accompany every lesson.
4. Presents an **interactive 5-question MCQ quiz** with instant feedback and detailed explanations.
5. Calculates a **100% accurate grade** using deterministic Python logic — not AI estimation.

The design follows a "Cozy Study Corner" aesthetic: warm tones, editorial typography, and smooth micro-animations to create an interface that feels as calming as it is powerful.

---

## Key Features

| Feature | Description |
|---|---|
| 🎓 **AI-Powered Lessons** | Generates 350–500 word explanations, structured into 4 pedagogical sections with analogies and real-world applications. |
| 📷 **Real-World Photography** | Automatically fetches high-quality educational photos from Wikimedia Commons. AI-powered search queries and SVG filtering ensure relevance. |
| 📝 **Interactive MCQ Quiz** | 5-question quiz with difficulty-scaled questions, hint system, and immediate answer reveals. |
| ✅ **Deterministic Grading** | Scores are calculated by direct Python index comparison — no AI "mercy points." |
| 💾 **Intelligent Caching** | Identical topic requests are served from the database instantly. |
| 🛠️ **Developer Mode** | Hidden JSON inspector, unlocked by clicking the logo 7 times. |
| 🌐 **Cloud-Native** | Fully stateless architecture with seamless dual support for local SQLite and cloud PostgreSQL (Neon). |
| 🎨 **Premium Design** | "Cozy Study Corner" aesthetic with glassmorphism, justified typography, Material 3 tokens, and smooth animations. |

---

## Tech Stack

### Backend
| Layer | Technology |
|---|---|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Runtime** | Python 3.10+ |
| **Database (Local)** | SQLite 3 |
| **Database (Cloud)** | [Neon PostgreSQL](https://neon.tech/) via `psycopg2` |
| **AI Integration** | [OpenRouter](https://openrouter.ai/) (Gemini 2.0 Flash Lite by default) |
| **Image Sourcing** | [Wikimedia Commons API](https://commons.wikimedia.org/w/api.php) |

### Frontend
| Layer | Technology |
|---|---|
| **Structure** | Vanilla HTML5 |
| **Styling** | [Tailwind CSS](https://tailwindcss.com/) (CDN) |
| **Typography** | Plus Jakarta Sans, Be Vietnam Pro (Google Fonts) |
| **Icons** | Material Symbols Outlined |
| **Logic** | Vanilla JavaScript (ES2020+) |

---

## Architecture

```
LearnNook/
│
├── [Browser] ── GET /static/index.html ──────────────────────────────────────────┐
│                                                                                   │
│   POST /api/session/start                                                         │
│   ┌─────────────────────────────────────────┐      ┌────────────────────────┐   │
│   │ 1. Check DB cache for topic             │──────│        SQLite /        │   │
│   │ 2. Call OpenRouter for Explanation      │      │    Neon PostgreSQL      │   │
│   │ 3. Call OpenRouter for MCQ Questions    │      └────────────────────────┘   │
│   │ 4. Search Wikimedia for real photo      │                                    │
│   │ 5. Download & save image locally*       │      ┌────────────────────────┐   │
│   │ 6. Save session & return to frontend    │──────│  Wikimedia Commons API │   │
│   └─────────────────────────────────────────┘      └────────────────────────┘   │
│                                       * Served from CDN on Vercel                │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

> **Brick Path Principle** 🧱: On local development, images are downloaded and served from `static/generated/` for maximum speed and reliability. On Vercel, they are served directly from Wikimedia's global CDN for stateless compatibility.

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **pip**
- An **[OpenRouter API Key](https://openrouter.ai/keys)** (free tier available)

### Local Development

**1. Clone the repository**
```bash
git clone https://github.com/Meera2906/learnnook.git
cd learnnook
```

**2. Create a virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure your environment**
```bash
cp .env.example .env
```
Open `.env` and add your OpenRouter key:
```env
OPENAI_API_KEY=your_openrouter_api_key_here
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

**6. Open the app**

Navigate to: [`http://localhost:8000`](http://localhost:8000)

---

## Deployment (Vercel + Neon)

### Step 1: Set Up Neon Database

1. Sign up at **[neon.tech](https://neon.tech)**.
2. Click **Create project** → Name it `LearnNook` → Select **PostgreSQL 16**.
3. On the dashboard, find **Connection Details** → enable **Connection Pooling**.
4. Copy the connection string (starts with `postgresql://...`).

### Step 2: Deploy to Vercel

1. Push your code to **GitHub**.
2. Sign up at **[vercel.com](https://vercel.com)** → **Add New... → Project** → Import your repository.
3. In the **Environment Variables** section, add the following:

| Key | Value |
|---|---|
| `OPENAI_API_KEY` | Your OpenRouter key |
| `DATABASE_URL` | Your Neon connection string |
| `LLM_MODEL` | `google/gemini-2.0-flash-lite-001` |
| `APP_TITLE` | `LearnNook` |
| `HTTP_REFERER` | Your Vercel URL (e.g., `https://learnnook.vercel.app`) |

4. Click **Deploy**. Your app will be live in ~60 seconds.

> **Note**: After deployment, access the app at [`https://learn-nook.vercel.app`](https://learn-nook.vercel.app) (it redirects automatically to the student dashboard).

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | — | OpenRouter API key for AI models |
| `DATABASE_URL` | ✅ Yes | `sqlite:///tutor.db` | Database connection string |
| `LLM_MODEL` | No | `google/gemini-2.0-flash-lite-001` | Model identifier for OpenRouter |
| `APP_TITLE` | No | `LearnNook` | Displayed in AI response headers |
| `HTTP_REFERER` | No | `http://localhost:8000` | Sent with API requests for rate-limiting. Set to `https://learn-nook.vercel.app` in production |

---

## Project Structure

```
learnnook/
│
├── main.py              # FastAPI application, routing, and AI pipeline
├── db.py                # Universal database layer (SQLite + PostgreSQL)
├── schemas.py           # Pydantic request/response models
├── prompts.py           # All AI prompt engineering (centralised)
│
├── static/
│   ├── index.html       # Full frontend SPA (all HTML, CSS, JS)
│   └── generated/       # Locally cached downloaded images (gitignored)
│
├── .env                 # Local secrets (gitignored)
├── .env.example         # Environment variable template
├── .gitignore           # Excludes secrets, DB, and generated images
├── vercel.json          # Vercel deployment configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

<div align="center">

Built with ❤️ and a lot of ☕ for curious minds everywhere.

*"The beautiful thing about learning is that no one can take it away from you."*

</div>
