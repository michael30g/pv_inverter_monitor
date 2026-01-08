class RegisterParser:
    def __init__(self, register_map: dict):
        self.map = register_map

    def parse(self, raw_registers: dict) -> dict:
        """
        raw_registers:
        {
          inverter_id: [reg0, reg1, reg2, ...]
        }
        """

        parsed = {}

        for inv_id, regs in raw_registers.items():
            parsed[inv_id] = {}

            for name, cfg in self.map.items():
                addr = cfg["address"]
                value = regs[addr]

                if cfg.get("unit") == "enum":
                    state_map = cfg.get("states", {})
                    parsed_value = state_map.get(str(value), "UNKNOWN")
                else:
                    parsed_value = value * cfg.get("scale", 1)

                parsed[inv_id][name] = {
                    "value": parsed_value,
                    "unit": cfg.get("unit"),
                }

        return parsed
