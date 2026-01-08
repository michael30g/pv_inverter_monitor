from simulation.mock_inverter import MockInverter
from devices.inverter_manager import InverterManager
import time


def main():
    manager = InverterManager()

    # Crear inversores simulados
    manager.add_inverter(1, MockInverter(slave_id=1))
    manager.add_inverter(2, MockInverter(slave_id=2))
    manager.add_inverter(3, MockInverter(slave_id=3))

    while True:
        data = manager.read_all(address=0, count=4)

        print("---- DATA SNAPSHOT ----")
        for inv_id, registers in data.items():
            print(f"Inverter {inv_id}: {registers}")

        time.sleep(2)


if __name__ == "__main__":
    main()
