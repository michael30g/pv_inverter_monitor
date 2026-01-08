from core.inverter_interface import InverterInterface
from core.logger import get_logger
import random


class MockInverter(InverterInterface):
    def __init__(self, slave_id: int):
        self.slave_id = slave_id
        self.logger = get_logger(f"MockInverter-{slave_id}")
        self.logger.info("Mock inverter initialized")

    def read_registers(self, address: int, count: int):
        self.logger.info(
            f"Reading registers | address={address} count={count}"
        )

        registers = []

        for offset in range(count):
            reg = address + offset

            if reg == 0:
                registers.append(random.randint(500, 2000))  # Power (W)
            elif reg == 1:
                registers.append(random.randint(480, 540))   # Battery V x10
            elif reg == 2:
                registers.append(random.randint(0, 200))     # Battery A x10
            elif reg == 3:
                registers.append(random.choice([0, 1, 2]))   # State
            else:
                registers.append(0)

        self.logger.info(f"Registers read: {registers}")
        return registers
