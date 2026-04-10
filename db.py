import sqlite3, json, uuid
from datetime import datetime

DB_PATH = "tutor.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                class_grade TEXT NOT NULL,
                subject TEXT NOT NULL,
                topic TEXT NOT NULL,
                explanation TEXT NOT NULL,
                questions TEXT NOT NULL,
                image_url TEXT,
                created_at TEXT NOT NULL
            )
        """)
        # Migration: Add image_url if it doesn't exist
        try:
            conn.execute("ALTER TABLE sessions ADD COLUMN image_url TEXT")
        except sqlite3.OperationalError:
            pass # Already exists

        conn.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                answers TEXT NOT NULL,
                score TEXT NOT NULL,
                feedback_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        """)
        # Index for cache lookups
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_cache
            ON sessions(class_grade, subject, topic)
        """)
        conn.commit()

def create_session(class_grade, subject, topic, explanation, questions, image_url=None):
    session_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO sessions 
               (id, class_grade, subject, topic, explanation, questions, image_url, created_at) 
               VALUES (?,?,?,?,?,?,?,?)""",
            (session_id, class_grade, subject, topic,
             explanation, json.dumps(questions), image_url,
             datetime.utcnow().isoformat())
        )
        conn.commit()
    return session_id

def get_session(session_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["questions"] = json.loads(d["questions"])
    return d

def get_cached_session(class_grade, subject, topic):
    """Return a cached explanation+questions for the same grade/subject/topic."""
    with get_conn() as conn:
        row = conn.execute(
            """SELECT explanation, questions, image_url FROM sessions
               WHERE class_grade=? AND subject=? AND topic=?
               ORDER BY created_at DESC LIMIT 1""",
            (class_grade, subject, topic)
        ).fetchone()
    if not row:
        return None
    return {
        "explanation": row["explanation"], 
        "questions": json.loads(row["questions"]),
        "image_url": row["image_url"]
    }

def save_response(session_id, answers, score, feedback_json):
    resp_id = str(uuid.uuid4())[:8]
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO responses 
               (id, session_id, answers, score, feedback_json, created_at) 
               VALUES (?,?,?,?,?,?)""",
            (resp_id, session_id, json.dumps(answers),
             score, json.dumps(feedback_json),
             datetime.utcnow().isoformat())
        )
        conn.commit()
    return resp_id

def get_responses(session_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM responses WHERE session_id=? ORDER BY created_at",
            (session_id,)
        ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        d["answers"] = json.loads(d["answers"])
        d["feedback_json"] = json.loads(d["feedback_json"])
        result.append(d)
    return result
