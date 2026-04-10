import os, urllib.parse, requests, uuid
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas import SessionStartRequest, EvaluateRequest, SessionStartResponse, EvaluateResponse, MCQQuestion
from prompts import build_explain_prompt, build_questions_prompt, build_evaluate_prompt
import db, json
from openai import AsyncOpenAI

load_dotenv()

app = FastAPI(title="LearnNook API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (though we'll use external URLs for dynamic images in this version)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenRouter Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "google/gemini-2.0-flash-lite-001"

client = AsyncOpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={
        "HTTP-Referer": os.getenv("HTTP_REFERER", "http://localhost:8000"),
        "X-Title": os.getenv("APP_TITLE", "LearnNook"),
    }
)

def cleanup_prompt(text: str, fallback: str) -> str:
    """Clean up AI-generated prompts for image URLs."""
    if not text or len(text.strip()) < 3:
        return urllib.parse.quote(fallback)
    # Remove characters that often break URLs or Pollinations
    clean = text.replace('"', '').replace("'", '').replace('\\', '').replace('\n', ' ')
    # Limit length to prevent URL overflow
    return urllib.parse.quote(clean[:200].strip())

def generate_and_store_image(visual_query: str, fallback_topic: str) -> str | None:
    """Searches for a real-world educational image on Wikimedia Commons and stores it locally."""
    try:
        # Step 1: Search for the topic on Wikimedia Commons
        # We request multiple results so we can filter out SVGs (charts)
        search_url = "https://commons.wikimedia.org/w/api.php"
        search_term = f"{visual_query} -filetype:svg -chart"
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "generator": "search",
            "gsrsearch": search_term,
            "gsrlimit": 5,
            "piprop": "original",
            "origin": "*"
        }
        
        print(f"Searching Wikimedia for: {search_term}")
        resp = requests.get(search_url, params=params, timeout=15, headers={"User-Agent": "LearnNook/1.0"})
        resp.raise_for_status()
        data = resp.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages:
            print(f"No results for: {search_term}. Trying fallback topic...")
            # Fallback to simple topic search
            params["gsrsearch"] = f"{fallback_topic} -filetype:svg"
            resp = requests.get(search_url, params=params, timeout=15, headers={"User-Agent": "LearnNook/1.0"})
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            if not pages: return None

        # Step 2: Filter for the first non-SVG result
        remote_url = None
        for page_id in pages:
            page = pages[page_id]
            source = page.get("original", {}).get("source")
            if source and not source.lower().endswith(".svg"):
                remote_url = source
                break
        
        if not remote_url:
            print("No non-SVG results found.")
            return None

        # VERCEL CHECK: Skip local storage if running on Vercel!
        if os.getenv("VERCEL"):
            print(f"Vercel detected: Serving remote image directly: {remote_url}")
            return remote_url

        # Step 3: Download and store locally
        out_dir = Path("static/generated")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        ext = os.path.splitext(remote_url)[1].lower() or '.jpg'
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = out_dir / filename

        print(f"Downloading real photo: {remote_url}")
        img_resp = requests.get(remote_url, timeout=30, headers={"User-Agent": "LearnNook/1.0"})
        img_resp.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(img_resp.content)

        return f"/static/generated/{filename}"
    except Exception as e:
        print("Real-world photo retrieval failed:", e)
        return None

def clean_json_response(text: str) -> dict:
    """Extra resilient JSON parsing for AI responses."""
    text = text.strip()
    # Remove markdown code blocks if the AI included them
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:].strip()
    
    # Simple strategy: find first '{' and last '}'
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        text = text[start:end+1]
        
    # Replace common unescaped character issues that break json.loads
    # (e.g., literal newlines inside strings are often a problem)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # If standard loads fails, we can try to fix simple escaped newline issues
        # and non-standard quotes if necessary, but for now we try a basic fix
        fixed_text = text.replace('\n', '\\n')
        # ... but wait, we need to be careful with real newlines outside strings
        # A safer bet is to use a slightly more complex cleaning if needed, 
        # but let's try the extraction first.
        return json.loads(text)

async def call_gpt(system: str, user: str) -> dict:
    """Single helper — all AI calls go through here for easy monitoring/caching."""
    model = os.getenv("LLM_MODEL", DEFAULT_MODEL)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
        max_tokens=2500, # Increased further and made more robust
    )
    text = response.choices[0].message.content
    try:
        return clean_json_response(text)
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        print(f"Raw Response: {text[:500]}...")
        raise HTTPException(500, f"AI returned invalid data format: {e}")

@app.on_event("startup")
async def startup():
    db.init_db()

@app.post("/api/session/start", response_model=SessionStartResponse)
async def start_session(req: SessionStartRequest):
    # Check cache first
    cached = db.get_cached_session(req.class_grade, req.subject, req.topic)
    if cached:
        # Check if cached data is in the old format (list of strings)
        raw_questions = cached["questions"]
        if raw_questions and (isinstance(raw_questions[0], str) or "correct_index" not in raw_questions[0] or "explanation" not in raw_questions[0]):
            # If old format or missing fields, we ignore cache and regenerate
            pass
        else:
            # Check if we have an image_url in cache, if not try to generate one
            image_url = cached.get("image_url")
            if not image_url:
                image_url = generate_and_store_image(req.topic, req.topic)
            
            session_id = db.create_session(req.class_grade, req.subject, req.topic,
                                            cached["explanation"], raw_questions, image_url)
            
            return SessionStartResponse(
                session_id=session_id,
                explanation=cached["explanation"],
                image_url=image_url,
                questions=[MCQQuestion(**q) for q in raw_questions],
                cached=True,
            )

    # Step 1: Generate detailed explanation
    sys1, usr1 = build_explain_prompt(req.class_grade, req.subject, req.topic)
    explain_data = await call_gpt(sys1, usr1)
    explanation = explain_data.get("explanation", "")
    visual_query = explain_data.get("visual_search_query", req.topic)

    if not explanation:
        raise HTTPException(500, "Failed to generate explanation")

    # Step 2: Generate 5 MCQs based on explanation
    sys2, usr2 = build_questions_prompt(req.class_grade, req.subject, req.topic, explanation)
    questions_data = await call_gpt(sys2, usr2)
    questions = questions_data.get("questions", [])

    if not questions or len(questions) < 5:
        raise HTTPException(500, f"Failed to generate 5 questions. Got {len(questions)}")

    # Step 3: Create image URL and store locally
    image_url = generate_and_store_image(visual_query, req.topic)

    # Save session with local image URL
    session_id = db.create_session(req.class_grade, req.subject, req.topic,
                                    explanation, questions, image_url)

    return SessionStartResponse(
        session_id=session_id,
        explanation=explanation,
        image_url=image_url,
        questions=[MCQQuestion(**q) for q in questions],
        cached=False,
    )

@app.post("/api/session/evaluate", response_model=EvaluateResponse)
async def evaluate_session(req: EvaluateRequest):
    session = db.get_session(req.session_id)
    if not session:
        raise HTTPException(404, "Session not found")

    # Questions are stored as JSON in DB, get_session loads them
    questions = session["questions"]

    # Step 1: Calculate score deterministically in Python
    correct_count = 0
    for i, q in enumerate(questions):
        if i < len(req.answers) and q.get("correct_index") == req.answers[i]:
            correct_count += 1
    actual_score = f"{correct_count}/{len(questions)}"

    # Step 2: Pass actual score to AI for feedback generation
    sys3, usr3 = build_evaluate_prompt(
        session["class_grade"],
        session["topic"],
        questions,
        req.answers,
        actual_score
    )
    eval_data = await call_gpt(sys3, usr3)

    # Use the Python-calculated score as the source of truth
    score = actual_score
    feedback = eval_data.get("feedback", "")
    per_question = eval_data.get("per_question", [])

    db.save_response(req.session_id, req.answers, score, eval_data)

    return EvaluateResponse(score=score, feedback=feedback, per_question=per_question)

@app.get("/api/session/{session_id}/history")
async def get_history(session_id: str):
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    responses = db.get_responses(session_id)
    return {"session": session, "responses": responses}

@app.get("/api/health")
async def health():
    return {"status": "ok"}
