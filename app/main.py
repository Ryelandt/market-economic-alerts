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
        token=os.environ.get("TELEGRAM_BOT_TOKEN"),
        chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
    )


    
# --- CALENDRIER DÉSACTIVÉ ---
    if not config["calendar"]["enabled"]:
        logger.info("Economic calendar is disabled. Nothing to process.")
        return

    # ⬇️ (Plus tard ici tu remettras une source macro)
    # source = ...
    # events = source.fetch_events()

    # for event in events:
    #     allowed, reason = decision_engine.should_alert(event)
    #     if allowed:
    #         telegram.send(event)



if __name__ == "__main__":
    main()
