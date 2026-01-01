from app.recommender.scoring.hybrid import HybridRecommender

_recommender = None

def get_recommender() -> HybridRecommender:
    global _recommender
    if _recommender is None:
        _recommender = HybridRecommender()
    return _recommender
