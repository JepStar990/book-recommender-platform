import duckdb
import numpy as np

DB_PATH = "data/books.duckdb"

def load_popularity():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT volume_id,
               COALESCE(ratings_count, 0) AS popularity
        FROM books
    """).fetch_df()
    con.close()
    return dict(zip(df["volume_id"], df["popularity"]))


def novelty(recommendations):
    popularity = load_popularity()
    pops = [popularity.get(r["volume_id"], 0) for r in recommendations]
    return 1 / (np.mean(pops) + 1)
