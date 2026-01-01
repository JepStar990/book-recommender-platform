import pickle
import numpy as np
from pathlib import Path

ARTIFACT_PATH = Path("ml/artifacts")

class CategorySimilarity:
    def __init__(self):
        with open(ARTIFACT_PATH / "category_matrix.pkl", "rb") as f:
            self.category_matrix = pickle.load(f)

        with open(ARTIFACT_PATH / "tfidf_volume_ids.pkl", "rb") as f:
            self.volume_ids = pickle.load(f)

        self.id_to_index = {
            vid: idx for idx, vid in enumerate(self.volume_ids)
        }

    def overlap_scores(self, volume_id: str):
        if volume_id not in self.id_to_index:
            return np.zeros(len(self.volume_ids))

        idx = self.id_to_index[volume_id]
        base = self.category_matrix[idx]

        overlap = self.category_matrix.dot(base)
        max_overlap = base.sum() if base.sum() > 0 else 1

        return overlap / max_overlap
