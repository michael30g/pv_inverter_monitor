import json


class Inverter:
    def __init__(self, slave_id: int, client, map_file: str):
        self.slave_id = slave_id
        self.client = client

        with open(map_file, "r", encoding="utf-8") as f:
            self.map = json.load(f)

    def read_all(self):
        """
        Lee todas las variables definidas en el mapa
        y devuelve un diccionario con valores escalados.
        """
        data = {}

        for name, cfg in self.map.items():
            register = cfg["register"]
            scale = cfg["scale"]

            raw_value = self.client.read_registers(register, 1)[0]
            data[name] = raw_value * scale

        return data
