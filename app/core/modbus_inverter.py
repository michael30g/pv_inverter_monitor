from core.inverter_interface import InverterInterface


class ModbusInverter(InverterInterface):
    def __init__(self, port: str, slave_id: int, baudrate=9600, timeout=1):
        self.port = port
        self.slave_id = slave_id
        self.baudrate = baudrate
        self.timeout = timeout

        # Cliente Modbus se inicializará luego
        self.client = None

    def connect(self):
        """
        Se conectará al bus RS485 (más adelante)
        """
        print(f"[INFO] Conectando a {self.port} (slave {self.slave_id})")

    def read_registers(self, address: int, count: int):
        """
        Lectura real Modbus (pendiente)
        """
        raise NotImplementedError("Modbus RTU aún no activado")
