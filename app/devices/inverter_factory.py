import json
from pathlib import Path

from simulation.mock_inverter import MockInverter
from core.modbus_inverter import ModbusInverter
from core.logger import get_logger


class InverterFactory:
    def __init__(self, config_path: Path):
        self.logger = get_logger("InverterFactory")
        self.config_path = config_path

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.mode = self.config.get("mode", "mock")
        self.logger.info(f"Factory mode: {self.mode}")

    def create_inverter(self, inverter_cfg: dict):
        if self.mode == "mock":
            return MockInverter(slave_id=inverter_cfg["slave_id"])

        if self.mode == "modbus":
            mb = self.config["modbus"]
            inverter = ModbusInverter(
                port=mb["port"],
                slave_id=inverter_cfg["slave_id"],
                baudrate=mb["baudrate"],
                timeout=mb["timeout"],
                retries=mb["retries"],
            )
            inverter.connect()
            return inverter

        raise ValueError(f"Unknown mode: {self.mode}")
