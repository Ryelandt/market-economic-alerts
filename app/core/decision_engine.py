def score_event(event):
    score = 0

    # importance officielle
    score += event.importance * 30

    # actifs surveillés (toi)
    tracked_assets = {"EURUSD", "XAUUSD", "BTCUSDT"}
    if tracked_assets.intersection(event.affected_assets):
        score += 30

    return score


def classify_event(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 50:
        return "IMPORTANT"
    return "IGNORE"
