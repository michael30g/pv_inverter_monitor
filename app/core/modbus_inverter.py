from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException

from core.inverter_interface import InverterInterface


class ModbusInverter(InverterInterface):
    def __init__(self, port: str, slave_id: int, baudrate=9600, timeout=1):
        self.port = port
        self.slave_id = slave_id
        self.baudrate = baudrate
        self.timeout = timeout

        self.client = ModbusSerialClient(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            parity='N',
            stopbits=1,
            bytesize=8
        )

    def connect(self):
        if not self.client.connect():
            raise ConnectionError(f"No se pudo conectar al puerto {self.port}")
        print(f"[INFO] RS485 conectado en {self.port}")

    def read_registers(self, address: int, count: int):
        try:
            result = self.client.read_holding_registers(
                address=address,
                count=count,
                slave=self.slave_id
            )

            if result.isError():
                raise ModbusIOException(result)

            return result.registers

        except Exception as e:
            print(f"[ERROR] Modbus read failed: {e}")
            return [None] * count

    def close(self):
        self.client.close()
