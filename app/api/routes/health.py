import time
from fastapi import APIRouter
import duckdb

DB_PATH = "data/books.duckdb"

router = APIRouter()
_start_time = time.time()


@router.get("/health")
def health():
    try:
        con = duckdb.connect(DB_PATH)
        row_count = con.execute("SELECT count(*) FROM books").fetchone()[0]
        con.close()
    except Exception:
        row_count = -1

    return {
        "status": "ok",
        "service": "book-recommender",
        "uptime_sec": round(time.time() - _start_time, 1),
        "books_in_db": row_count,
    }
