from pathlib import Path
import time

from devices.inverter_factory import InverterFactory
from devices.inverter_manager import InverterManager
from collector import Collector


def main():
    # 1️⃣ Ruta al JSON
    config_path = Path(__file__).parent / "config" / "inverter_map.json"

    # 2️⃣ Factory
    factory = InverterFactory(config_path)

    # 3️⃣ Manager
    manager = InverterManager()

    # 4️⃣ Crear inversores
    for inv_cfg in factory.config["inverters"]:
        inverter = factory.create_inverter(inv_cfg)
        manager.add_inverter(inv_cfg["id"], inverter)

    # 5️⃣ Collector (cliente → servidor)
    collector = Collector(
        manager=manager,
        server_url="http://127.0.0.1:8000"
    )

    # 6️⃣ Ejecutar loop
    collector.run(interval=2)


if __name__ == "__main__":
    main()
