import os
import json
import urllib.request


def send_alert(event, level):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        raise RuntimeError("Telegram credentials not set")

    message = (
        f"🚨 ALERTE {level}\n\n"
        f"📅 {event.name}\n"
        f"⏰ {event.datetime}\n\n"
        "Impact probable :\n"
        + "\n".join(f"• {a}" for a in event.affected_assets)
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        print("Telegram response:", response_body)

