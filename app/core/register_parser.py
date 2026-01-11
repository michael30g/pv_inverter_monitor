class RegisterParser:
    def __init__(self, register_map: dict):
        self.register_map = register_map

    def parse(self, registers: list) -> dict:
        parsed = {}

        for name, cfg in self.register_map.items():
            addr = cfg["address"]
            scale = cfg.get("scale", 1)

            raw = registers[addr]
            value = raw * scale

            if cfg.get("unit") == "enum":
                states = cfg.get("states", {})
                value = states.get(str(raw), "UNKNOWN")

            parsed[name] = value

        return parsed
