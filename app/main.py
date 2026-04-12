import yaml
import logging
import os

from app.core.decision_engine import DecisionEngine
from app.alerts.telegram_alert import TelegramAlert
from app.models.event import Event
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("macro-alerts")


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    logger.info("Application started")

    decision_engine = DecisionEngine()

    telegram = TelegramAlert(
        token=os.environ.get("TELEGRAM_BOT_TOKEN"),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
    )
  # ✅ EVENT MOCK
    event = Event(
        datetime=datetime.utcnow() + timedelta(minutes=10),
        currency="USD",
        title="✅ TEST TELEGRAM ALERT",
        impact_level="HIGH",
        description="This is a manual test event",
        risk="No risk - test only",
        market_bias="NEUTRAL",
    )

    telegram.send(event)
    logger.info("Test Telegram alert sent successfully")  


if __name__ == "__main__":
    main()
