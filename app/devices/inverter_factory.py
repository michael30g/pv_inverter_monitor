import json
from pathlib import Path

from core.logger import get_logger
from simulation.mock_inverter import MockInverter
from core.modbus_inverter import ModbusInverter


class InverterFactory:
    """
    Crea instancias de inversores (mock o modbus real)
    a partir del archivo de configuración JSON
    """

    def __init__(self, config_path: Path):
        self.logger = get_logger("InverterFactory")

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.mode = self.config.get("mode", "mock")
        self.logger.info(f"Factory mode: {self.mode}")

    def create_inverter(self, inverter_cfg: dict):
        if self.mode == "mock":
            return MockInverter(slave_id=inverter_cfg["slave_id"])

        elif self.mode == "modbus":
            modbus_cfg = self.config["modbus"]
            return ModbusInverter(
                slave_id=inverter_cfg["slave_id"],
                port=modbus_cfg["port"],
                baudrate=modbus_cfg["baudrate"],
                timeout=modbus_cfg["timeout"],
            )

        else:
            raise ValueError(f"Unknown inverter mode: {self.mode}")
