import os
import requests

def send_alert(event, level):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print("BOT TOKEN =", os.getenv("TELEGRAM_BOT_TOKEN"))
    print("CHAT ID   =", os.getenv("TELEGRAM_CHAT_ID"))
    
    if not bot_token or not chat_id:
        raise RuntimeError("Telegram credentials not set")

    message = (
        f"🚨 ALERTE {level}\n\n"
        f"📅 {event.name}\n"
    )
