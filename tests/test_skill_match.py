import pytest
from app.recommender.models.skill_match import SkillMatcher


class TestSkillMatcher:
    def test_exact_match_beginner(self):
        sm = SkillMatcher()
        assert sm.score("beginner", "beginner") == 1.0

    def test_exact_match_intermediate(self):
        sm = SkillMatcher()
        assert sm.score("intermediate", "intermediate") == 1.0

    def test_exact_match_advanced(self):
        sm = SkillMatcher()
        assert sm.score("advanced", "advanced") == 1.0

    def test_progression_beginner_to_intermediate(self):
        sm = SkillMatcher()
        assert sm.score("beginner", "intermediate") == 0.5

    def test_progression_intermediate_to_advanced(self):
        sm = SkillMatcher()
        assert sm.score("intermediate", "advanced") == 0.5

    def test_no_match_beginner_to_advanced(self):
        sm = SkillMatcher()
        assert sm.score("beginner", "advanced") == 0.0

    def test_reverse_progression(self):
        sm = SkillMatcher()
        assert sm.score("advanced", "beginner") == 0.0
        assert sm.score("intermediate", "beginner") == 0.0
        assert sm.score("advanced", "intermediate") == 0.0
