import duckdb
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle

DB_PATH = "data/books.duckdb"
ARTIFACT_PATH = Path("ml/artifacts")
ARTIFACT_PATH.mkdir(parents=True, exist_ok=True)


def load_books():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT
            volume_id,
            title,
            COALESCE(description, '') AS description
        FROM books
    """).fetch_df()
    con.close()
    return df

def build_tfidf(df: pd.DataFrame):
    # Explicit sanitization (critical)
    df["title"] = df["title"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)

    df["text"] = (df["title"] + " " + df["description"]).str.strip()

    # Drop rows with no usable text
    df = df[df["text"] != ""]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=10_000,
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(df["text"])

    with open(ARTIFACT_PATH / "tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    with open(ARTIFACT_PATH / "tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)

    # Save aligned volume_ids (VERY important later)
    with open(ARTIFACT_PATH / "tfidf_volume_ids.pkl", "wb") as f:
        pickle.dump(df["volume_id"].tolist(), f)

    return tfidf_matrix
