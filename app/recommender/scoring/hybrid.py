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

        # Safety check
        assert len(self.volume_ids) == self.category.category_matrix.shape[0]

    def recommend(self, volume_id: str, top_n: int = 10):
        content_scores = self.content.similarity_scores(volume_id)
        category_scores = self.category.overlap_scores(volume_id)
        target_level = self.skill_levels.get(volume_id)

        results = []

        for idx, vid in enumerate(self.volume_ids):
            if vid == volume_id:
                continue

            content = content_scores[idx]
            category = category_scores[idx]
            popularity = self.popularity.get(vid, 0)
            skill = self.skill_matcher.score(
                target_level,
                self.skill_levels.get(vid)
            )

            final_score = (
                0.45 * content +
                0.25 * category +
                0.20 * popularity +
                0.10 * skill
            )

            results.append({
                "volume_id": vid,
                "score": final_score,
                "signals": {
                    "content_similarity": content,
                    "category_overlap": category,
                    "popularity": popularity,
                    "skill_match": skill
                }
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_n]
