from app.sources.auto_calendar import fetch_events
from app.core.decision_engine import score_event, classify_event
from app.alerts.telegram_alert import send_daily_summary

def main():
    events = fetch_events()

    important_events = []

    for event in events:
        score = score_event(event)
        level = classify_event(score)

        if level in ("CRITICAL", "IMPORTANT"):
            important_events.append(event)

    send_daily_summary(important_events)

if __name__ == "__main__":
    main()
