"""
Sri Eshwar College of Engineering - Campus Skill Exchange
Database initialization and connection management using SQLite.
"""

import sqlite3
from contextlib import contextmanager
from typing import Generator
from config import DATABASE_PATH

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    department TEXT NOT NULL,
    year_of_study TEXT NOT NULL,
    bio TEXT DEFAULT '',
    learning_interests TEXT DEFAULT '',
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    is_paid BOOLEAN DEFAULT 0,
    price REAL DEFAULT 0.0,
    modes TEXT NOT NULL, -- JSON or comma-separated e.g. "ONLINE,ON_CAMPUS,ASYNCHRONOUS"
    availability TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS session_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER,
    learner_id INTEGER NOT NULL,
    tutor_id INTEGER NOT NULL,
    mode TEXT NOT NULL, -- ONLINE, ON_CAMPUS
    session_date TEXT NOT NULL, -- YYYY-MM-DD
    session_time TEXT NOT NULL, -- HH:MM
    meeting_spot TEXT DEFAULT '', -- Required for ON_CAMPUS
    google_meet_link TEXT DEFAULT '', -- Populated when tutor accepts
    is_demo_link BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT '',
    status TEXT DEFAULT 'pending', -- pending, accepted, declined, completed
    price REAL DEFAULT 0.0,
    commission_amount REAL DEFAULT 0.0,
    tutor_response_note TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(id) ON DELETE SET NULL,
    FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS async_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    learner_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    title TEXT NOT NULL,
    question_text TEXT NOT NULL,
    code_snippet TEXT DEFAULT '',
    status TEXT DEFAULT 'open', -- open, answered, closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS async_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    tutor_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_accepted BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES async_questions(id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER UNIQUE NOT NULL, -- Prevents duplicate reviews for same session
    learner_id INTEGER NOT NULL,
    tutor_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES session_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (learner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS commission_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    tutor_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    commission_rate REAL NOT NULL,
    commission_amount REAL NOT NULL,
    tutor_earnings REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES session_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def init_db() -> None:
    """Initialize database tables."""
    with get_db_connection() as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized successfully at {DATABASE_PATH}")
