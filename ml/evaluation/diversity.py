import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

ARTIFACT_PATH = Path("ml/artifacts")

def intra_list_diversity(volume_ids):
    with open(ARTIFACT_PATH / "tfidf_matrix.pkl", "rb") as f:
        tfidf = pickle.load(f)
    with open(ARTIFACT_PATH / "tfidf_volume_ids.pkl", "rb") as f:
        all_ids = pickle.load(f)

    index = {vid: i for i, vid in enumerate(all_ids)}
    indices = [index[v] for v in volume_ids if v in index]

    if len(indices) < 2:
        return 0.0

    sims = cosine_similarity(tfidf[indices])
    return 1 - sims.mean()
