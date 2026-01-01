import duckdb
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from pathlib import Path
import pickle

DB_PATH = "data/books.duckdb"
ARTIFACT_PATH = Path("ml/artifacts")

def build_category_features():
    # Load canonical volume IDs (from TF-IDF)
    with open(ARTIFACT_PATH / "tfidf_volume_ids.pkl", "rb") as f:
        canonical_ids = pickle.load(f)

    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT volume_id, category
        FROM categories
    """).fetch_df()
    con.close()

    grouped = df.groupby("volume_id")["category"].apply(list).to_dict()

    # Align categories to canonical index
    aligned_categories = [
        grouped.get(vid, []) for vid in canonical_ids
    ]

    mlb = MultiLabelBinarizer()
    category_matrix = mlb.fit_transform(aligned_categories)

    with open(ARTIFACT_PATH / "category_binarizer.pkl", "wb") as f:
        pickle.dump(mlb, f)

    with open(ARTIFACT_PATH / "category_matrix.pkl", "wb") as f:
        pickle.dump(category_matrix, f)

    return canonical_ids, category_matrix
