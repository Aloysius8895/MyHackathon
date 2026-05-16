import sqlite3
import json
from datetime import datetime

DB_PATH = "ecolink.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,  -- 'company', 'mentor', 'partner'
            industry TEXT,
            description TEXT,
            skills TEXT,         -- JSON array
            location TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS linkages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_a_id INTEGER,
            actor_b_id INTEGER,
            linkage_type TEXT,   -- 'mentor-company', 'partner-programme', etc.
            status TEXT DEFAULT 'active',  -- 'active', 'completed', 'archived'
            match_score REAL,
            match_reason TEXT,
            programme TEXT,
            score_breakdown TEXT,  -- JSON: per-dimension scores from the formula engine
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (actor_a_id) REFERENCES actors(id),
            FOREIGN KEY (actor_b_id) REFERENCES actors(id)
        )
    """)

    # Safe migration: add score_breakdown to existing databases that don't have it yet
    try:
        c.execute("ALTER TABLE linkages ADD COLUMN score_breakdown TEXT")
        conn.commit()
    except Exception:
        pass  # Column already exists

    c.execute("""
        CREATE TABLE IF NOT EXISTS engagements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            linkage_id INTEGER,
            outcome TEXT,        -- 'successful', 'partial', 'unsuccessful'
            notes TEXT,
            rating INTEGER,      -- 1-5
            recorded_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (linkage_id) REFERENCES linkages(id)
        )
    """)

    conn.commit()
    conn.close()


# --- Actors ---

def add_actor(name, actor_type, industry, description, skills, location):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO actors (name, type, industry, description, skills, location) VALUES (?,?,?,?,?,?)",
        (name, actor_type, industry, description, json.dumps(skills), location)
    )
    conn.commit()
    actor_id = c.lastrowid
    conn.close()
    return actor_id


def get_actors(actor_type=None):
    conn = get_conn()
    c = conn.cursor()
    if actor_type:
        c.execute("SELECT * FROM actors WHERE type=? ORDER BY created_at DESC", (actor_type,))
    else:
        c.execute("SELECT * FROM actors ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    for r in rows:
        r["skills"] = json.loads(r["skills"]) if r["skills"] else []
    return rows


def get_actor(actor_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM actors WHERE id=?", (actor_id,))
    row = c.fetchone()
    conn.close()
    if row:
        r = dict(row)
        r["skills"] = json.loads(r["skills"]) if r["skills"] else []
        return r
    return None


# --- Linkages ---

def create_linkage(actor_a_id, actor_b_id, linkage_type, match_score, match_reason,
                   programme, score_breakdown=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO linkages (actor_a_id, actor_b_id, linkage_type, match_score, match_reason, programme, score_breakdown) VALUES (?,?,?,?,?,?,?)",
        (actor_a_id, actor_b_id, linkage_type, match_score, match_reason, programme,
         json.dumps(score_breakdown) if score_breakdown else None)
    )
    conn.commit()
    linkage_id = c.lastrowid
    conn.close()
    return linkage_id


def get_linkages():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT l.*,
               a.name as actor_a_name, a.type as actor_a_type,
               b.name as actor_b_name, b.type as actor_b_type
        FROM linkages l
        JOIN actors a ON l.actor_a_id = a.id
        JOIN actors b ON l.actor_b_id = b.id
        ORDER BY l.created_at DESC
    """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def update_linkage_status(linkage_id, status):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE linkages SET status=? WHERE id=?", (status, linkage_id))
    conn.commit()
    conn.close()


# --- Engagements ---

def add_engagement(linkage_id, outcome, notes, rating):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO engagements (linkage_id, outcome, notes, rating) VALUES (?,?,?,?)",
        (linkage_id, outcome, notes, rating)
    )
    conn.commit()
    conn.close()


def get_engagements(linkage_id=None):
    conn = get_conn()
    c = conn.cursor()
    if linkage_id:
        c.execute("""
            SELECT e.*, l.linkage_type, a.name as actor_a_name, b.name as actor_b_name
            FROM engagements e
            JOIN linkages l ON e.linkage_id = l.id
            JOIN actors a ON l.actor_a_id = a.id
            JOIN actors b ON l.actor_b_id = b.id
            WHERE e.linkage_id=?
            ORDER BY e.recorded_at DESC
        """, (linkage_id,))
    else:
        c.execute("""
            SELECT e.*, l.linkage_type, a.name as actor_a_name, b.name as actor_b_name
            FROM engagements e
            JOIN linkages l ON e.linkage_id = l.id
            JOIN actors a ON l.actor_a_id = a.id
            JOIN actors b ON l.actor_b_id = b.id
            ORDER BY e.recorded_at DESC
        """)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_stats():
    conn = get_conn()
    c = conn.cursor()
    stats = {}
    c.execute("SELECT COUNT(*) as count FROM actors")
    stats["total_actors"] = c.fetchone()["count"]
    c.execute("SELECT COUNT(*) as count FROM actors WHERE type='mentor'")
    stats["mentors"] = c.fetchone()["count"]
    c.execute("SELECT COUNT(*) as count FROM actors WHERE type='company'")
    stats["companies"] = c.fetchone()["count"]
    c.execute("SELECT COUNT(*) as count FROM linkages")
    stats["total_linkages"] = c.fetchone()["count"]
    c.execute("SELECT COUNT(*) as count FROM linkages WHERE status='active'")
    stats["active_linkages"] = c.fetchone()["count"]
    c.execute("SELECT AVG(rating) as avg FROM engagements")
    avg = c.fetchone()["avg"]
    stats["avg_rating"] = round(avg, 1) if avg else 0
    conn.close()
    return stats
