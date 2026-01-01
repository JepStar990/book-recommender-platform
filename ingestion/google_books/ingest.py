import json
from ingestion.google_books.client import GoogleBooksClient
from ingestion.google_books.schemas import normalize_volume
from app.db.duckdb_client import get_connection

def ingest_query(query: str, max_pages: int = 5):
    client = GoogleBooksClient()
    conn = get_connection()

    start_index = 0
    for _ in range(max_pages):
        response = client.search(query=query, start_index=start_index)

        items = response.get("items", [])
        if not items:
            break

        for volume in items:
            record = normalize_volume(volume)

            conn.execute("""
            INSERT OR IGNORE INTO books VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
            )
            """, (
                record["volume_id"],
                record["title"],
                record["description"],
                record["published_date"],
                record["page_count"],
                record["language"],
                record["average_rating"],
                record["ratings_count"],
                record["preview_link"],
                record["info_link"],
                json.dumps(record["raw_json"])
            ))

            for author in record["authors"]:
                conn.execute("""
                INSERT OR IGNORE INTO authors VALUES (?, ?)
                """, (record["volume_id"], author))

            for category in record["categories"]:
                conn.execute("""
                INSERT OR IGNORE INTO categories VALUES (?, ?)
                """, (record["volume_id"], category))

        start_index += len(items)

    conn.close()
