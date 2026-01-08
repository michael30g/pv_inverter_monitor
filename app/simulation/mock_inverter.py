from core.inverter_interface import InverterInterface
import random


class MockInverter(InverterInterface):
    def __init__(self, slave_id: int):
        self.slave_id = slave_id

    def read_registers(self, address: int, count: int):
        """
        Simula la lectura de registros Modbus.
        Devuelve una lista de enteros como lo haría un inversor real.
        """
        registers = []

        for offset in range(count):
            reg = address + offset

            if reg == 0:
                # Potencia instantánea (W)
                registers.append(random.randint(500, 2000))
            elif reg == 1:
                # Voltaje batería (48.0 – 54.0 V) escalado x10
                registers.append(random.randint(480, 540))
            elif reg == 2:
                # Corriente batería (0.0 – 20.0 A) escalado x10
                registers.append(random.randint(0, 200))
            elif reg == 3:
                # Estado del inversor
                # 0 = OFF, 1 = ON, 2 = FAULT
                registers.append(random.choice([0, 1, 2]))
            else:
                registers.append(0)

        return registers
