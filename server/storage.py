from typing import Dict, List
from models import InverterTelemetry


class InMemoryStorage:
    def __init__(self):
        self.data: Dict[int, List[InverterTelemetry]] = {}

    def save(self, telemetry: InverterTelemetry):
        if telemetry.inverter_id not in self.data:
            self.data[telemetry.inverter_id] = []
        self.data[telemetry.inverter_id].append(telemetry)

    def get_latest(self) -> Dict[int, InverterTelemetry]:
        return {
            inv_id: records[-1]
            for inv_id, records in self.data.items()
            if records
        }
