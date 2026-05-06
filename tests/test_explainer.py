from app.recommender.explainability.explainer import explain


class TestExplainer:
    def test_high_content_similarity(self):
        signals = {
            "content_similarity": 0.8,
            "category_overlap": 0.0,
            "popularity": 0.0,
            "skill_match": 0.0,
        }
        reasons = explain(signals)
        assert "Very similar topics and descriptions" in reasons

    def test_moderate_content_similarity(self):
        signals = {
            "content_similarity": 0.5,
            "category_overlap": 0.0,
            "popularity": 0.0,
            "skill_match": 0.0,
        }
        reasons = explain(signals)
        assert "Related subject matter" in reasons

    def test_no_content_similarity(self):
        signals = {
            "content_similarity": 0.1,
            "category_overlap": 0.0,
            "popularity": 0.0,
            "skill_match": 0.0,
        }
        reasons = explain(signals)
        assert len(reasons) == 0

    def test_category_overlap(self):
        signals = {
            "content_similarity": 0.0,
            "category_overlap": 0.5,
            "popularity": 0.0,
            "skill_match": 0.0,
        }
        reasons = explain(signals)
        assert "Shares the same categories" in reasons

    def test_high_popularity(self):
        signals = {
            "content_similarity": 0.0,
            "category_overlap": 0.0,
            "popularity": 0.7,
            "skill_match": 0.0,
        }
        reasons = explain(signals)
        assert "Highly rated and frequently reviewed" in reasons

    def test_exact_skill_match(self):
        signals = {
            "content_similarity": 0.0,
            "category_overlap": 0.0,
            "popularity": 0.0,
            "skill_match": 1.0,
        }
        reasons = explain(signals)
        assert "Matches your skill level" in reasons

    def test_progression_skill_match(self):
        signals = {
            "content_similarity": 0.0,
            "category_overlap": 0.0,
            "popularity": 0.0,
            "skill_match": 0.5,
        }
        reasons = explain(signals)
        assert "Good next-step progression" in reasons

    def test_all_signals(self):
        signals = {
            "content_similarity": 0.9,
            "category_overlap": 1.0,
            "popularity": 0.8,
            "skill_match": 1.0,
        }
        reasons = explain(signals)
        assert len(reasons) >= 4

    def test_returns_list_of_strings(self):
        signals = {
            "content_similarity": 0.5,
            "category_overlap": 0.5,
            "popularity": 0.5,
            "skill_match": 0.5,
        }
        reasons = explain(signals)
        assert isinstance(reasons, list)
        for r in reasons:
            assert isinstance(r, str)
