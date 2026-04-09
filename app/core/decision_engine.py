from datetime import datetime, timedelta
from typing import Tuple
from app.models.event import Event


class DecisionEngine:
    ALERT_WINDOW = timedelta(hours=2)

    def should_alert(self, event: Event) -> Tuple[bool, str]:
        now = datetime.utcnow()

        if event.datetime <= now:
            return False, "Event already passed"

        if event.datetime - now > self.ALERT_WINDOW:
            return False, "Event too far"

        if event.impact_level != "HIGH":
            return False, "Impact insufficient"

        return True, "High-impact macro event imminent"
