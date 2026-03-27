from app.sources.auto_calendar import fetch_events
from app.core.decision_engine import score_event, classify_event
from app.alerts.telegram_alert import send_alert

def main():
    events = fetch_events()

    for event in events:
        score = score_event(event)
        level = classify_event(score)

        if level != "IGNORE":
            send_alert(event, level)

if __name__ == "__main__":
    main()
