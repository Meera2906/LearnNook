# LearnNook 📚

**LearnNook** is a premium, AI-powered educational platform designed to turn any topic into a cozy, interactive study corner. It leverages LLMs to generate high-fidelity lessons and real-world educational photography to provide an immersive learning experience.

## ✨ Features

- **Cozy Study Corner UI**: A premium, editorial-grade interface with justified text, custom typography, and a "distraction-free" design.
- **Photorealistic Sourcing**: Automatically fetches high-quality, academic photos from **Wikimedia Commons** for every topic.
- **Interactive Quizzes**: 5-question MCQs with deterministic grading and encouraging AI-generated explanations.
- **Local Resilience**: Images are searched, downloaded, and stored locally on your backend for maximum reliability and speed.
- **Rich Text Formatting**: Supports inline highlights, custom dividers, and structured subheadings.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [OpenRouter API Key](https://openrouter.ai/keys)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/learnnook.git
   cd learnnook
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Copy the example environment file and add your OpenRouter key:
   ```bash
   cp .env.example .env
   # Edit .env and paste your OPENAI_API_KEY
   ```

### Running Locally

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Open your browser to:
`http://localhost:8000/static/index.html`

## 🧱 Architecture

- **Backend**: FastAPI (Python)
- **Database**: SQLite (SQLAlchemy)
- **Frontend**: Vanilla HTML5 / Tailwind CSS / JavaScript
- **AI Integration**: OpenRouter (GPT/Flash models)
- **Image Provider**: Wikimedia Commons API

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ for curious minds.
