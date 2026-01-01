def explain(content, category, popularity, skill):
    reasons = []

    if content > 0.6:
        reasons.append("Very similar content")
    elif content > 0.3:
        reasons.append("Related topics")

    if category > 0:
        reasons.append("Shared categories")

    if popularity > 0.5:
        reasons.append("Popular among readers")

    if skill == 1.0:
        reasons.append("Matches your skill level")

    return reasons
