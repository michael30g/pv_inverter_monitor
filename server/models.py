from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class InverterTelemetry(BaseModel):
    inverter_id: int
    timestamp: datetime
    data: Dict[str, float | str]
