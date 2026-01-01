import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

ARTIFACT_PATH = Path("ml/artifacts")

class ContentBasedRecommender:
    def __init__(self):
        with open(ARTIFACT_PATH / "tfidf_matrix.pkl", "rb") as f:
            self.tfidf_matrix = pickle.load(f)

        with open(ARTIFACT_PATH / "tfidf_volume_ids.pkl", "rb") as f:
            self.volume_ids = pickle.load(f)

        self.id_to_index = {
            vid: idx for idx, vid in enumerate(self.volume_ids)
        }

    def similarity_scores(self, volume_id: str):
        if volume_id not in self.id_to_index:
            raise ValueError("Volume ID not found in TF-IDF index")

        idx = self.id_to_index[volume_id]
        scores = cosine_similarity(
            self.tfidf_matrix[idx],
            self.tfidf_matrix
        ).flatten()

        return scores
