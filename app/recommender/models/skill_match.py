from app.features.skill_level.classifier import classify_skill_level

class SkillMatcher:
    def load(self):
        df = classify_skill_level()
        return dict(zip(df["volume_id"], df["skill_level"]))

    def score(self, target_level, candidate_level):
        if target_level == candidate_level:
            return 1.0
        if target_level == "beginner" and candidate_level == "intermediate":
            return 0.5
        if target_level == "intermediate" and candidate_level == "advanced":
            return 0.5
        return 0.0
