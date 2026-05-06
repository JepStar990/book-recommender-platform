import duckdb
import pandas as pd
import re

DB_PATH = "data/books.duckdb"

BEGINNER_KEYWORDS = [
    "introduction", "intro to", "beginners", "beginner", "getting started",
    "fundamentals", "basic", "basics", "primer", "crash course", "dummies",
    "101", "first course", "easy guide", "simple guide", "step by step",
]
INTERMEDIATE_KEYWORDS = [
    "intermediate", "practical", "applied", "cookbook", "recipes",
    "patterns", "in action", "effective", "handbook", "guide",
]
ADVANCED_KEYWORDS = [
    "advanced", "expert", "mastering", "definitive", "complete",
    "comprehensive", "professional", "in depth", "deep dive",
    "architecture", "internals", "theory of", "mathematics of",
]


def classify_skill_level():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT volume_id, page_count, title, description
        FROM books
    """).fetch_df()
    con.close()

    def infer_level(row):
        title = str(row["title"]).lower() if not pd.isna(row["title"]) else ""
        desc = str(row["description"]).lower() if not pd.isna(row["description"]) else ""
        text = title + " " + desc
        pages = int(row["page_count"]) if not pd.isna(row["page_count"]) else 0

        beginner_score = sum(1 for kw in BEGINNER_KEYWORDS if kw in text)
        intermediate_score = sum(1 for kw in INTERMEDIATE_KEYWORDS if kw in text)
        advanced_score = sum(1 for kw in ADVANCED_KEYWORDS if kw in text)

        if pages > 0:
            if pages < 200:
                beginner_score += 1
            elif pages < 500:
                intermediate_score += 1
            else:
                advanced_score += 1

        scores = {
            "beginner": beginner_score,
            "intermediate": intermediate_score,
            "advanced": advanced_score,
        }
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "intermediate"
        return best

    df["skill_level"] = df.apply(infer_level, axis=1)
    return df[["volume_id", "skill_level"]]
