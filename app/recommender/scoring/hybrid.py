import numpy as np
from app.recommender.models.content_based import ContentBasedRecommender
from app.recommender.models.category_similarity import CategorySimilarity
from app.recommender.models.popularity import PopularityModel
from app.recommender.models.skill_match import SkillMatcher

class HybridRecommender:
    def __init__(self):
        self.content = ContentBasedRecommender()
        self.category = CategorySimilarity()
        self.popularity = PopularityModel().load()
        self.skill_levels = SkillMatcher().load()
        self.skill_matcher = SkillMatcher()

        self.volume_ids = self.content.volume_ids

        assert len(self.content.volume_ids) == self.category.category_matrix.shape[0], \
            "Feature matrices are misaligned"

    def recommend(self, volume_id: str, top_n: int = 10):
        content_scores = self.content.similarity_scores(volume_id)
        category_scores = self.category.overlap_scores(volume_id)

        target_level = self.skill_levels.get(volume_id)

        final_scores = []

        for idx, vid in enumerate(self.volume_ids):
            if vid == volume_id:
                continue

            score = (
                0.45 * content_scores[idx] +
                0.25 * category_scores[idx] +
                0.20 * self.popularity.get(vid, 0) +
                0.10 * self.skill_matcher.score(
                    target_level,
                    self.skill_levels.get(vid)
                )
            )

            final_scores.append((vid, score))

        final_scores.sort(key=lambda x: x[1], reverse=True)
        return final_scores[:top_n]
