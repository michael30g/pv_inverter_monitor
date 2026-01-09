from pathlib import Path
import time
from core.alarm_engine import AlarmEngine


from devices.inverter_manager import InverterManager
from devices.inverter_factory import InverterFactory
from core.register_parser import RegisterParser


def main():
    # Ruta al archivo de configuración
    config_path = Path(__file__).parent / "config" / "inverter_map.json"

    # Inicialización
    factory = InverterFactory(config_path)
    manager = InverterManager()

    # Crear parser de registros (UNA sola vez)
    parser = RegisterParser(factory.config["register_map"])
    alarm_engine = AlarmEngine(factory.config["limits"])

    # Crear e insertar inversores
    for inv in factory.config["inverters"]:
        inverter = factory.create_inverter(inv)
        manager.add_inverter(inv["id"], inverter)

    try:
        while True:
            # Leer registros crudos
            raw_data = manager.read_all(address=0, count=4)

            # Parsear a valores físicos
            parsed_data = parser.parse(raw_data)
            alarms = alarm_engine.evaluate(parsed_data)

            for inv_id, inv_alarms in alarms.items():
                for alarm in inv_alarms:
                    print(
                        f"ALARM | Inverter {inv_id} | "
                        f"{alarm['signal']} = {alarm['value']} "
                        f"({alarm['severity']})"
                    )


            print("---- DATA SNAPSHOT ----")
            for inv_id, values in parsed_data.items():
                print(f"Inverter {inv_id}:")
                for name, info in values.items():
                    print(f"  {name}: {info['value']} {info['unit']}")

            time.sleep(2)

    except KeyboardInterrupt:
        print("Shutting down monitor...")


if __name__ == "__main__":
    main()
