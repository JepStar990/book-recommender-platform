import duckdb
from app.recommender.scoring.hybrid import HybridRecommender

DB_PATH = "data/books.duckdb"

def load_categories():
    con = duckdb.connect(DB_PATH)
    rows = con.execute("""
        SELECT volume_id, category
        FROM categories
    """).fetchall()
    con.close()

    cat_map = {}
    for vid, cat in rows:
        cat_map.setdefault(vid, set()).add(cat)
    return cat_map


def precision_at_k(k=5, sample_size=50):
    recommender = HybridRecommender()
    categories = load_categories()

    volume_ids = list(categories.keys())[:sample_size]
    scores = []

    for vid in volume_ids:
        recs = recommender.recommend(vid, top_n=k)
        if not recs:
            continue

        relevant = 0
        for r in recs:
            if categories.get(vid, set()) & categories.get(r["volume_id"], set()):
                relevant += 1

        scores.append(relevant / k)

    return sum(scores) / len(scores)
