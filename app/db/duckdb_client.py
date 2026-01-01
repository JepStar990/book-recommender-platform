import duckdb
from pathlib import Path

DB_PATH = Path("data/books.duckdb")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
        volume_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        published_date TEXT,
        page_count INTEGER,
        language TEXT,
        average_rating DOUBLE,
        ratings_count INTEGER,
        preview_link TEXT,
        info_link TEXT,
        raw_json JSON,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        volume_id TEXT,
        author TEXT,
        PRIMARY KEY (volume_id, author)
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        volume_id TEXT,
        category TEXT,
        PRIMARY KEY (volume_id, category)
    )
    """)

    conn.close()
