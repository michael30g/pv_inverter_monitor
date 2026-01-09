from typing import Dict, List
from core.logger import get_logger
from core.inverter_interface import InverterInterface


class InverterManager:
    """
    Gestiona múltiples inversores (mock o reales)
    """

    def __init__(self):
        self.logger = get_logger("InverterManager")
        self.inverters: Dict[int, InverterInterface] = {}
        self.logger.info("Inverter manager initialized")

    def add_inverter(self, inverter_id: int, inverter: InverterInterface):
        self.inverters[inverter_id] = inverter
        self.logger.info(f"Inverter added | id={inverter_id}")

    def get_snapshot(self):
    
        snapshot = {}

        for inv_id, inverter in self.inverters.items():
            try:
                registers = inverter.read_registers(address=0, count=4)

                snapshot[inv_id] = {
                    "power_w": registers[0],
                    "battery_voltage_v": registers[1] / 10.0,
                    "battery_current_a": registers[2] / 10.0,
                    "state": registers[3],
                }

            except Exception as e:
                snapshot[inv_id] = {"error": str(e)}

        return snapshot


    def read_all(self, address: int, count: int) -> Dict[int, List[int]]:
        self.logger.info(
            f"Reading all inverters | address={address} count={count}"
        )

        data = {}

        for inv_id, inverter in self.inverters.items():
            try:
                data[inv_id] = inverter.read_registers(address, count)
            except Exception as e:
                self.logger.error(
                    f"Error reading inverter {inv_id}: {e}"
                )

        return data
