import duckdb
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from pathlib import Path
import pickle

DB_PATH = "data/books.duckdb"
ARTIFACT_PATH = Path("ml/artifacts")

def build_category_features():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT volume_id, category
        FROM categories
    """).fetch_df()
    con.close()

    grouped = df.groupby("volume_id")["category"].apply(list).reset_index()

    mlb = MultiLabelBinarizer()
    category_matrix = mlb.fit_transform(grouped["category"])

    with open(ARTIFACT_PATH / "category_binarizer.pkl", "wb") as f:
        pickle.dump(mlb, f)

    with open(ARTIFACT_PATH / "category_matrix.pkl", "wb") as f:
        pickle.dump(category_matrix, f)

    return grouped["volume_id"], category_matrix
