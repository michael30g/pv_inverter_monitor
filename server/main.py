from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class InverterTelemetry(BaseModel):
    power_w: float
    battery_voltage: float
    battery_current: float
    state: str


class TelemetrySnapshot(BaseModel):
    timestamp: datetime
    inverters: Dict[int, InverterTelemetry]


@app.get("/")
def root():
    return {"status": "server running"}


@app.post("/telemetry")
def receive_telemetry(snapshot: TelemetrySnapshot):
    logging.info(f"Received telemetry: {snapshot}")
    return {"status": "ok"}
