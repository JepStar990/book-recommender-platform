from app.db.duckdb_client import init_db
from ingestion.google_books.ingest import ingest_query

QUERIES = [
    "data science",
    "machine learning",
    "python programming",
    "statistics",
    "artificial intelligence"
]

if __name__ == "__main__":
    init_db()

    for q in QUERIES:
        print(f"Ingesting query: {q}")
        ingest_query(q, max_pages=5)

    print("Ingestion completed successfully.")
