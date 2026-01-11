import random
from core.inverter_interface import InverterInterface


class MockInverter(InverterInterface):
    """
    Simula un inversor solar para pruebas sin hardware
    """

    def __init__(self, slave_id: int):
        self.slave_id = slave_id

    def read_registers(self, address: int, count: int):
        # Simulación simple de registros
        power = random.randint(0, 5000)          # W
        voltage = random.randint(480, 560)       # 48.0–56.0 V
        current = random.randint(-100, 100)      # -10.0–10.0 A
        state = random.choice([0, 1])             # 0=idle,1=active

        return [
            power,
            voltage,
            current,
            state,
        ]
