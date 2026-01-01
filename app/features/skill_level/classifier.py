import duckdb
import pandas as pd

DB_PATH = "data/books.duckdb"

def classify_skill_level():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT volume_id, page_count, title
        FROM books
    """).fetch_df()
    con.close()

    def infer_level(row):
        title = str(row["title"]).lower() if not pd.isna(row["title"]) else ""
        pages = int(row["page_count"]) if not pd.isna(row["page_count"]) else 0

        if "introduction" in title or pages < 200:
            return "beginner"
        elif pages < 400:
            return "intermediate"
        else:
            return "advanced"

    df["skill_level"] = df.apply(infer_level, axis=1)
    return df[["volume_id", "skill_level"]]
