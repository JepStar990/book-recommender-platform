import os
from app.db.duckdb_client import init_db
from ingestion.google_books.ingest import ingest_query

MAX_PAGES = int(os.getenv("INGESTION_MAX_PAGES_PER_QUERY", "3"))

QUERIES = [
    # Computer Science & Programming
    "python programming",
    "javascript programming",
    "java programming",
    "c programming",
    "go programming language",
    "rust programming",
    "algorithms and data structures",
    "software engineering",
    "computer systems architecture",
    "database design",
    "operating systems",
    "computer networks",
    "cybersecurity",
    "web development",
    "mobile app development",
    "game programming",

    # Data Science, ML & AI
    "data science",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "computer vision",
    "big data analytics",
    "data engineering",

    # Mathematics & Statistics
    "statistics textbook",
    "linear algebra",
    "calculus textbook",
    "probability theory",
    "discrete mathematics",
    "numerical methods",

    # Science
    "physics textbook",
    "chemistry textbook",
    "biology textbook",
    "astronomy",
    "neuroscience",
    "genetics",

    # Engineering
    "electrical engineering",
    "mechanical engineering",
    "civil engineering",
    "chemical engineering",

    # Business & Economics
    "business strategy",
    "marketing",
    "entrepreneurship",
    "finance textbook",
    "economics textbook",
    "investing",
    "management leadership",
    "accounting",

    # Humanities & Social Sciences
    "world history",
    "philosophy",
    "psychology textbook",
    "sociology",
    "political science",
    "international relations",
    "linguistics",

    # Arts & Design
    "graphic design",
    "art history",
    "photography",
    "music theory",
    "creative writing",
    "film studies",

    # Practical & Lifestyle
    "cookbook",
    "travel guide",
    "personal finance",
    "self improvement",
    "productivity",
    "health and wellness",

    # Education & Reference
    "english grammar",
    "study skills",
    "encyclopedia",
    "academic writing",

    # Fiction genres (to capture popular books)
    "science fiction novels",
    "fantasy novels",
    "mystery thriller novels",
    "literary fiction",
    "historical fiction",
    "romance novels",
    "horror novels",
    "graphic novels",
]

if __name__ == "__main__":
    init_db()

    for i, q in enumerate(QUERIES, 1):
        print(f"[{i}/{len(QUERIES)}] Ingesting: {q}")
        ingest_query(q, max_pages=MAX_PAGES)

    print(f"Ingestion completed — {len(QUERIES)} queries processed.")
