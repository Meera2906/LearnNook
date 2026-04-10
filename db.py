import os, sqlite3, json, uuid
from datetime import datetime

# Attempt to import psycopg2 for Postgres support
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tutor.db")

def get_conn():
    """Returns a connection based on the DATABASE_URL environment variable."""
    if DATABASE_URL.startswith("postgresql"):
        if not psycopg2:
            raise ImportError("psycopg2-binary is required for PostgreSQL support but not installed.")
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        conn.autocommit = True # Make it behave like our previous wrapper
        return conn
    else:
        # Local SQLite
        path = DATABASE_URL.replace("sqlite:///", "")
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn

def execute(query, params=()):
    """Executes a query and handles the ? vs %s syntax difference."""
    is_postgres = DATABASE_URL.startswith("postgresql")
    if is_postgres:
        query = query.replace("?", "%s")
    
    with get_conn() as conn:
        if is_postgres:
            cur = conn.cursor()
            cur.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                res = cur.fetchall()
                return [dict(r) for r in res]
            return []
        else:
            # SQLite
            cur = conn.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                res = cur.fetchall()
                return [dict(r) for r in res]
            conn.commit()
            return []

def init_db():
    """Initializes the database schema for the active engine."""
    # SQLite-specific migration logic handled gracefully
    is_sqlite = not DATABASE_URL.startswith("postgresql")
    
    execute("""
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
    if is_sqlite:
        try: execute("ALTER TABLE sessions ADD COLUMN image_url TEXT")
        except: pass
    
    execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            answers TEXT NOT NULL,
            score TEXT NOT NULL,
            feedback_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Create index for caching speed
    if is_sqlite:
        execute("CREATE INDEX IF NOT EXISTS idx_session_cache ON sessions(class_grade, subject, topic)")
    else:
        # Postgres version (if index exists error is handled by IF NOT EXISTS usually)
        try: execute("CREATE INDEX idx_session_cache ON sessions(class_grade, subject, topic)")
        except: pass

def create_session(class_grade, subject, topic, explanation, questions, image_url=None):
    session_id = str(uuid.uuid4())[:8]
    execute(
        """INSERT INTO sessions 
           (id, class_grade, subject, topic, explanation, questions, image_url, created_at) 
           VALUES (?,?,?,?,?,?,?,?)""",
        (session_id, class_grade, subject, topic,
         explanation, json.dumps(questions), image_url,
         datetime.utcnow().isoformat())
    )
    return session_id

def get_session(session_id):
    rows = execute("SELECT * FROM sessions WHERE id=?", (session_id,))
    if not rows: return None
    d = rows[0]
    d["questions"] = json.loads(d["questions"])
    return d

def get_cached_session(class_grade, subject, topic):
    rows = execute(
        """SELECT explanation, questions, image_url FROM sessions
           WHERE class_grade=? AND subject=? AND topic=?
           ORDER BY created_at DESC LIMIT 1""",
        (class_grade, subject, topic)
    )
    if not rows: return None
    row = rows[0]
    return {
        "explanation": row["explanation"], 
        "questions": json.loads(row["questions"]),
        "image_url": row["image_url"]
    }

def save_response(session_id, answers, score, feedback_json):
    resp_id = str(uuid.uuid4())[:8]
    execute(
        """INSERT INTO responses 
           (id, session_id, answers, score, feedback_json, created_at) 
           VALUES (?,?,?,?,?,?)""",
        (resp_id, session_id, json.dumps(answers),
         score, json.dumps(feedback_json),
         datetime.utcnow().isoformat())
    )
    return resp_id

def get_responses(session_id):
    rows = execute("SELECT * FROM responses WHERE session_id=? ORDER BY created_at", (session_id,))
    result = []
    for row in rows:
        d = row
        d["answers"] = json.loads(d["answers"])
        d["feedback_json"] = json.loads(d["feedback_json"])
        result.append(d)
    return result
