import time
import requests
from datetime import datetime
from core.logger import get_logger


STATE_MAP = {
    0: "OFF",
    1: "ON",
    2: "FAULT"
}


class Collector:
    def __init__(self, manager, server_url: str):
        self.manager = manager
        self.server_url = server_url.rstrip("/")
        self.logger = get_logger("Collector")

    def _build_payload(self):
        snapshot = self.manager.get_snapshot()

        inverters_payload = {}

        for inv_id, data in snapshot.items():
            if "error" in data:
                continue

            inverters_payload[str(inv_id)] = {
                "power_w": data["power_w"],
                "battery_voltage": data["battery_voltage_v"],
                "battery_current": data["battery_current_a"],
                "state": STATE_MAP.get(data["state"], "UNKNOWN")
            }

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "inverters": inverters_payload
        }

        return payload

    def run(self, interval: int = 2):
        self.logger.info("Collector started, sending data to server")

        while True:
            payload = self._build_payload()

            print("SENDING PAYLOAD:", payload)

            try:
                response = requests.post(
                    f"{self.server_url}/telemetry",
                    json=payload,
                    timeout=5
                )

                if response.status_code == 200:
                    self.logger.info("Snapshot sent successfully")
                else:
                    self.logger.warning(
                        f"Server responded with status {response.status_code}: {response.text}"
                    )

            except Exception as e:
                self.logger.error(f"Error sending data: {e}")

            time.sleep(interval)
