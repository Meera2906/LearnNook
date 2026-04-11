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
- [Sample Input & Output](#sample-input--output)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
- [Deployment (Vercel + Neon)](#deployment-vercel--neon)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Scale Considerations](#scale-considerations)
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

## Sample Input & Output

### Input

```json
{
  "class_grade": "8th",
  "subject": "Science",
  "topic": "Photosynthesis"
}
```

---

### Output 1 — `POST /api/session/start`

```json
{
  "session_id": "a3f2b1c9",
  "cached": false,
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/.../Leaf_macro.jpg",
  "explanation": "### The Secret Life of Leaves 🌿\n\nHave you ever wondered how a tree feeds itself without ever moving? Plants are master chefs — and their kitchen is a single leaf.\n\n---\n\n### The Core Concept ⚡\n\nPhotosynthesis is the process by which green plants use ==sunlight==, ==water==, and ==carbon dioxide== to produce their own food in the form of ==glucose==. This happens inside tiny structures called ==chloroplasts==, which contain a green pigment called ==chlorophyll== — the same thing that makes leaves green.\n\nThe equation looks like this:\n6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂\n\nIn plain English: the plant takes in carbon dioxide from the air through tiny pores called ==stomata==, absorbs water from the soil through its roots, and uses energy from sunlight to convert them into glucose (its food) and oxygen (which it releases back into the air).\n\n---\n\n### The Analogy 🍳\n\nThink of a leaf as a solar-powered kitchen. The chlorophyll acts like solar panels, capturing energy from the sun. The carbon dioxide and water are the raw ingredients. The glucose produced is the finished meal — and the oxygen released is like the steam that escapes while cooking.\n\n---\n\n### Real-World Application 🌍\n\nEvery breath you take is possible because of photosynthesis. The oxygen in Earth's atmosphere was produced by plants and algae over billions of years. Farmers also use this knowledge — they ensure crops get enough sunlight and water to maximise photosynthesis, directly increasing food yield.",
  "questions": [
    {
      "question": "What are the three raw materials required for photosynthesis?",
      "options": [
        "Oxygen, glucose, and sunlight",
        "Carbon dioxide, water, and sunlight",
        "Nitrogen, water, and moonlight",
        "Carbon dioxide, oxygen, and soil"
      ],
      "correct_index": 1,
      "explanation": "Plants absorb CO₂ from the air, water from the soil, and capture light energy using chlorophyll — these three are converted into glucose and oxygen.",
      "hint": "Think about what a plant absorbs from its environment to make food."
    },
    {
      "question": "Where exactly inside a plant cell does photosynthesis take place?",
      "options": [
        "The nucleus",
        "The mitochondria",
        "The chloroplast",
        "The cell wall"
      ],
      "correct_index": 2,
      "explanation": "Chloroplasts contain chlorophyll, the pigment that captures sunlight. This is where the light reactions and the Calvin cycle both occur.",
      "hint": "It's the green-coloured organelle."
    },
    {
      "question": "What is the primary product of photosynthesis that the plant uses as food?",
      "options": [
        "Oxygen",
        "Carbon dioxide",
        "Water",
        "Glucose"
      ],
      "correct_index": 3,
      "explanation": "Glucose (C₆H₁₂O₆) is the sugar the plant synthesises and uses as its primary energy source for growth and cellular processes.",
      "hint": "It's a type of sugar — the plant's energy currency."
    },
    {
      "question": "A plant is placed in a dark room for 48 hours. What will most likely happen to the rate of photosynthesis?",
      "options": [
        "It will increase because the plant works harder",
        "It will stay the same — light is not needed",
        "It will stop completely because light energy is unavailable",
        "It will slow down slightly but continue"
      ],
      "correct_index": 2,
      "explanation": "Light is a fundamental raw material. Without it, chlorophyll cannot capture energy and the entire process halts — though the plant can survive short periods using stored glucose.",
      "hint": "Consider what role light plays as an ingredient, not just a condition."
    },
    {
      "question": "Farmers growing crops in greenhouses sometimes pump extra CO₂ into the air. Why?",
      "options": [
        "To keep pests away from the plants",
        "To increase the rate of photosynthesis and boost yield",
        "To replace the oxygen consumed by the plants",
        "To keep the temperature inside stable"
      ],
      "correct_index": 1,
      "explanation": "CO₂ is a limiting factor in photosynthesis. Increasing its concentration allows the plant to produce more glucose faster, directly improving crop growth and yield.",
      "hint": "Think about what happens when you give a chef more of their key ingredient."
    }
  ]
}
```

---

### Output 2 — `POST /api/session/evaluate`

**Request:**
```json
{
  "session_id": "a3f2b1c9",
  "answers": [1, 2, 3, 2, 1]
}
```

**Response:**
```json
{
  "score": "4/5",
  "feedback": "Excellent work! You have a strong grasp of photosynthesis — from the raw materials right down to real-world applications. One small mix-up on the chloroplast question, but your understanding of the big picture is clear. Keep it up!",
  "per_question": [
    {
      "correct": true,
      "comment": "Perfect! You identified all three raw materials correctly.",
      "explanation": "Carbon dioxide enters through stomata, water is absorbed via roots, and sunlight is captured by chlorophyll — all three are essential and cannot be substituted."
    },
    {
      "correct": true,
      "comment": "Spot on! The chloroplast is the powerhouse of photosynthesis.",
      "explanation": "Chloroplasts are unique to plant cells and contain chlorophyll. The light-dependent reactions happen in the thylakoid membranes, and the Calvin cycle occurs in the stroma."
    },
    {
      "correct": true,
      "comment": "Great — glucose is the plant's food, not oxygen.",
      "explanation": "Oxygen is a by-product released into the atmosphere. Glucose is retained by the plant and used for energy, growth, and stored as starch."
    },
    {
      "correct": false,
      "comment": "Not quite — darkness completely halts photosynthesis.",
      "explanation": "Without light, chlorophyll cannot absorb energy, so neither the light-dependent nor light-independent reactions can proceed. The rate drops to zero, not just slows down."
    },
    {
      "correct": true,
      "comment": "Excellent real-world application thinking!",
      "explanation": "CO₂ is often the limiting factor in photosynthesis. By increasing its concentration, farmers effectively remove that bottleneck, allowing plants to photosynthesise faster and produce more biomass."
    }
  ]
}
```

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

## Scale Considerations

> **Assignment question: If 10,000 students use this daily — what breaks first, and how do you fix it?**

**What breaks first:** The LLM API rate limits and per-minute token limits on OpenRouter/Gemini at peak load.

At 10K students × 2 API calls (explain + questions) = ~20K calls/day with spikes hitting rate limits during school hours (9am–3pm).

**Fixes, in order of priority:**

| Problem | Fix |
|---|---|
| Repeated topic calls hitting the API | **Already implemented** — DB caching serves identical grade+subject+topic from Postgres instantly |
| Peak hour rate limit spikes | **Async job queue** — Celery + Redis; students get a "preparing your lesson" screen while it processes |
| Cost at scale | **Already using Gemini Flash Lite** — ~10× cheaper than GPT-4. Popular topics cached = near-zero marginal cost |
| Wikimedia image fetch latency | **Pre-warm cache** — nightly cron job pre-generates lessons for the top 50 topics per grade |
| Single Vercel instance bottleneck | **Horizontal scaling** — Vercel auto-scales functions; move to PostgreSQL connection pooling (Neon already supports this) |

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

<div align="center">

Built with ❤️ and a lot of ☕ for curious minds everywhere.

*"The beautiful thing about learning is that no one can take it away from you."*

</div>
