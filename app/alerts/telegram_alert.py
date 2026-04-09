import requests
import logging

from app.models.event import Event

logger = logging.getLogger(__name__)


class TelegramAlert:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, event: Event) -> None:
        message = (
            f"🚨 MACRO EVENT ALERT 🚨\n\n"
            f"Event: {event.title}\n"
            f"Currency: {event.currency}\n"
            f"Time: {event.datetime}\n"
            f"Impact: {event.impact_level}\n"
            f"Risk: {event.risk}\n"
            f"Bias: {event.market_bias}"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
        }

        try:
            response = requests.post(self.url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram alert sent successfully")
        except Exception as e:
            logger.error(f"Telegram alert failed: {e}")
