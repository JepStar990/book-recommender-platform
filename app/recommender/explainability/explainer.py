def explain(signals: dict) -> list[str]:
    reasons = []

    if signals["content_similarity"] > 0.6:
        reasons.append("Very similar topics and descriptions")
    elif signals["content_similarity"] > 0.3:
        reasons.append("Related subject matter")

    if signals["category_overlap"] > 0:
        reasons.append("Shares the same categories")

    if signals["popularity"] > 0.5:
        reasons.append("Highly rated and frequently reviewed")

    if signals["skill_match"] == 1.0:
        reasons.append("Matches your skill level")
    elif signals["skill_match"] == 0.5:
        reasons.append("Good next-step progression")

    return reasons
