def send_alert(event, level):
    print("\n==============================")
    print(f"🚨 ALERT LEVEL: {level}")
    print(f"📅 Event: {event.name}")
    print(f"⏰ Time: {event.datetime}")
    print("📊 Affected Assets:")
    for asset in event.affected_assets:
        print(f" - {asset}")
    print("==============================\n")
