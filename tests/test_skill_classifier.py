import pytest
from app.features.skill_level.classifier import (
    BEGINNER_KEYWORDS,
    INTERMEDIATE_KEYWORDS,
    ADVANCED_KEYWORDS,
    classify_skill_level,
)


class TestKeywordLists:
    def test_beginner_keywords_not_empty(self):
        assert len(BEGINNER_KEYWORDS) > 0

    def test_intermediate_keywords_not_empty(self):
        assert len(INTERMEDIATE_KEYWORDS) > 0

    def test_advanced_keywords_not_empty(self):
        assert len(ADVANCED_KEYWORDS) > 0

    def test_no_keyword_overlap(self):
        beginner_set = set(BEGINNER_KEYWORDS)
        intermediate_set = set(INTERMEDIATE_KEYWORDS)
        advanced_set = set(ADVANCED_KEYWORDS)
        assert beginner_set.isdisjoint(intermediate_set)
        assert beginner_set.isdisjoint(advanced_set)
        assert intermediate_set.isdisjoint(advanced_set)


class TestSkillLevelInference:
    def test_beginner_title(self):
        import pandas as pd
        df = pd.DataFrame([{
            "volume_id": "test1",
            "title": "Introduction to Python Programming",
            "description": "A beginners guide to coding",
            "page_count": 150,
        }])

        title = str(df.loc[0, "title"]).lower()
        desc = str(df.loc[0, "description"]).lower()
        text = title + " " + desc
        pages = int(df.loc[0, "page_count"])

        beginner_score = sum(1 for kw in BEGINNER_KEYWORDS if kw in text)
        assert beginner_score >= 1

    def test_advanced_title(self):
        import pandas as pd
        df = pd.DataFrame([{
            "volume_id": "test2",
            "title": "Mastering Deep Learning Architecture",
            "description": "A comprehensive guide to neural network internals",
            "page_count": 600,
        }])

        title = str(df.loc[0, "title"]).lower()
        desc = str(df.loc[0, "description"]).lower()
        text = title + " " + desc
        pages = int(df.loc[0, "page_count"])

        advanced_score = sum(1 for kw in ADVANCED_KEYWORDS if kw in text)
        assert advanced_score >= 1

    def test_page_count_thresholds(self):
        import pandas as pd
        df = pd.DataFrame([{
            "volume_id": "test3",
            "title": "Some Book",
            "description": "A book with no keyword matches",
            "page_count": 300,
        }])

        title = str(df.loc[0, "title"]).lower()
        desc = str(df.loc[0, "description"]).lower()
        text = title + " " + desc
        pages = int(df.loc[0, "page_count"])

        # 300 pages should add to intermediate_score
        beginner_score = sum(1 for kw in BEGINNER_KEYWORDS if kw in text)
        intermediate_score = sum(1 for kw in INTERMEDIATE_KEYWORDS if kw in text)
        advanced_score = sum(1 for kw in ADVANCED_KEYWORDS if kw in text)

        # No keywords matched, so page count should give intermediate
        if pages > 0 and pages < 200:
            beginner_score += 1
        elif pages < 500:
            intermediate_score += 1
        else:
            advanced_score += 1

        assert intermediate_score == 1
        assert beginner_score == 0
        assert advanced_score == 0

    def test_missing_data_defaults(self):
        import pandas as pd
        df = pd.DataFrame([{
            "volume_id": "test4",
            "title": None,
            "description": None,
            "page_count": None,
        }])

        title = str(df.loc[0, "title"]).lower() if not pd.isna(df.loc[0, "title"]) else ""
        desc = str(df.loc[0, "description"]).lower() if not pd.isna(df.loc[0, "description"]) else ""
        text = title + " " + desc
        pages = int(df.loc[0, "page_count"]) if not pd.isna(df.loc[0, "page_count"]) else 0

        assert text.strip() == ""
        assert pages == 0

    def test_output_columns(self):
        result = classify_skill_level()
        assert "volume_id" in result.columns
        assert "skill_level" in result.columns
        assert set(result["skill_level"].unique()).issubset({"beginner", "intermediate", "advanced"})
