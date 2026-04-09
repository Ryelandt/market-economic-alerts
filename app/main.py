import yaml
import logging
from app.sources.auto_calendar import AutoCalendarSource
from app.core.decision_engine import DecisionEngine
from app.alerts.telegram_alert import TelegramAlert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("macro-alerts")


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    source = AutoCalendarSource(config["calendar"]["api_key"])
    decision_engine = DecisionEngine()
    telegram = TelegramAlert(
        token=config["telegram"]["token"],
        chat_id=config["telegram"]["chat_id"],
    )

    for event in source.fetch_events():
        allowed, reason = decision_engine.should_alert(event)
        logger.info(f"{event.title} → {reason}")

        if allowed:
            telegram.send(event)


if __name__ == "__main__":
    main()
