import duckdb
import numpy as np
import pandas as pd

DB_PATH = "data/books.duckdb"

def build_popularity():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT
            volume_id,
            COALESCE(average_rating, 0) AS rating,
            COALESCE(ratings_count, 0) AS count
        FROM books
    """).fetch_df()
    con.close()

    df["popularity_score"] = df["rating"] * np.log1p(df["count"])
    return df[["volume_id", "popularity_score"]]
