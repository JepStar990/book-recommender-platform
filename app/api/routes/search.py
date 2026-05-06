import os
import json
import logging
from fastapi import APIRouter, Query
import duckdb

from ingestion.google_books.client import GoogleBooksClient
from ingestion.google_books.schemas import normalize_volume

DB_PATH = "data/books.duckdb"
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY") or None

router = APIRouter()
logger = logging.getLogger(__name__)


def _ingest_batch(volumes: list) -> int:
    ingested = 0
    con = duckdb.connect(DB_PATH)
    for volume in volumes:
        try:
            record = normalize_volume(volume)
            con.execute("""
                INSERT OR IGNORE INTO books VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
                )
            """, (
                record["volume_id"], record["title"], record["description"],
                record["published_date"], record["page_count"], record["language"],
                record["average_rating"], record["ratings_count"],
                record["preview_link"], record["info_link"],
                json.dumps(record["raw_json"])
            ))
            for author in record["authors"]:
                con.execute(
                    "INSERT OR IGNORE INTO authors VALUES (?, ?)",
                    (record["volume_id"], author)
                )
            for category in record["categories"]:
                con.execute(
                    "INSERT OR IGNORE INTO categories VALUES (?, ?)",
                    (record["volume_id"], category)
                )
            ingested += 1
        except Exception:
            pass
    con.close()
    return ingested


@router.get("/search")
def search_books(q: str = Query(..., min_length=2), limit: int = 10):
    con = duckdb.connect(DB_PATH)
    results = con.execute("""
        SELECT volume_id, title, description, average_rating, ratings_count
        FROM books
        WHERE lower(title) LIKE ? OR lower(description) LIKE ?
        LIMIT ?
    """, (f"%{q.lower()}%", f"%{q.lower()}%", limit)).fetchall()
    con.close()

    books = [
        {
            "volume_id": r[0], "title": r[1], "description": r[2],
            "average_rating": r[3], "ratings_count": r[4],
            "source": "local"
        }
        for r in results
    ]

    if len(books) < limit and API_KEY:
        try:
            client = GoogleBooksClient(api_key=API_KEY)
            response = client.search(query=q, max_results=limit - len(books))
            items = response.get("items", [])

            new_books = []
            for item in items:
                info = item.get("volumeInfo", {})
                new_books.append({
                    "volume_id": item.get("id"),
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "average_rating": info.get("averageRating"),
                    "ratings_count": info.get("ratingsCount"),
                    "source": "google_books"
                })

            _ingest_batch(items)

            seen_ids = {b["volume_id"] for b in books}
            for nb in new_books:
                if nb["volume_id"] not in seen_ids:
                    books.append(nb)
        except Exception as e:
            logger.warning(f"Google Books fallback failed: {e}")

    return books
