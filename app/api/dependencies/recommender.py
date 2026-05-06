import threading
from app.recommender.scoring.hybrid import HybridRecommender

_recommender = None
_lock = threading.Lock()


def get_recommender() -> HybridRecommender:
    global _recommender
    if _recommender is None:
        with _lock:
            if _recommender is None:
                _recommender = HybridRecommender()
    return _recommender
