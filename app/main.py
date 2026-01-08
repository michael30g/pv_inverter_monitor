import json
from simulation.mock_inverter import MockInverter


def load_register_map(path: str):
    with open(path, "r") as f:
        return json.load(f)


def read_inverter(inverter, register_map):
    data = {}

    for name, cfg in register_map.items():
        reg = cfg["register"]
        scale = cfg["scale"]
        unit = cfg["unit"]

        raw = inverter.read_registers(reg, 1)[0]
        value = raw * scale

        data[name] = {
            "value": value,
            "unit": unit,
            "raw": raw
        }

    return data


def main():
    inverter = MockInverter(slave_id=1)
    register_map = load_register_map("config/inverter_map.json")

    data = read_inverter(inverter, register_map)

    print("\n=== DATOS DEL INVERSOR ===")
    for k, v in data.items():
        print(f"{k}: {v['value']} {v['unit']} (raw={v['raw']})")


if __name__ == "__main__":
    main()
