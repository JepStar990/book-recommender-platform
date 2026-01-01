from fastapi import APIRouter, Query
import duckdb

DB_PATH = "data/books.duckdb"

router = APIRouter()

@router.get("/search")
def search_books(q: str = Query(..., min_length=2), limit: int = 10):
    con = duckdb.connect(DB_PATH)
    results = con.execute("""
        SELECT volume_id, title
        FROM books
        WHERE lower(title) LIKE ?
        LIMIT ?
    """, (f"%{q.lower()}%", limit)).fetchall()
    con.close()

    return [
        {"volume_id": r[0], "title": r[1]}
        for r in results
    ]
