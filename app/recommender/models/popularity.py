import duckdb
import numpy as np

DB_PATH = "data/books.duckdb"

class PopularityModel:
    def load(self):
        con = duckdb.connect(DB_PATH)
        df = con.execute("""
            SELECT
                volume_id,
                COALESCE(average_rating, 0) * log(1 + COALESCE(ratings_count, 0)) AS score
            FROM books
        """).fetch_df()
        con.close()

        max_score = df["score"].max() or 1
        return dict(zip(df["volume_id"], df["score"] / max_score))
