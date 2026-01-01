from fastapi import APIRouter, Depends, Query, HTTPException
import duckdb
from app.api.dependencies.recommender import get_recommender
from app.recommender.explainability.explainer import explain

DB_PATH = "data/books.duckdb"

router = APIRouter()

@router.get("/recommend/by-book")
def recommend_by_book(
    volume_id: str = Query(...),
    top_n: int = Query(5, ge=1, le=20),
    recommender = Depends(get_recommender)
):
    try:
        results = recommender.recommend(volume_id, top_n=top_n)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")

    con = duckdb.connect(DB_PATH)

    response = []
    for r in results:
        vid = r["volume_id"]
        row = con.execute("""
            SELECT title
            FROM books
            WHERE volume_id = ?
        """, (vid,)).fetchone()

        response.append({
            "volume_id": vid,
            "title": row[0] if row else None,
            "score": float(r["score"]),
            "reasons": explain(r["signals"])
        })

    con.close()
    return response
