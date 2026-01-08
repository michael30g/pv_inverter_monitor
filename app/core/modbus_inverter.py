from pymodbus.client import ModbusSerialClient
from core.inverter_interface import InverterInterface
from core.logger import get_logger
import time


class ModbusInverter(InverterInterface):
    """
    Inversor real vía Modbus RTU (RS485)
    """

    def __init__(
        self,
        port: str,
        slave_id: int,
        baudrate: int = 9600,
        timeout: float = 1.0,
        retries: int = 3,
    ):
        self.slave_id = slave_id
        self.retries = retries
        self.logger = get_logger(f"ModbusInverter-{slave_id}")

        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            parity="N",
            stopbits=1,
            bytesize=8,
        )

        self.logger.info(
            f"Modbus inverter created | port={port} slave={slave_id}"
        )

    def connect(self) -> bool:
        if not self.client.connect():
            self.logger.error("Failed to connect to Modbus device")
            return False

        self.logger.info("Modbus connection established")
        return True

    def read_registers(self, address: int, count: int):
        for attempt in range(1, self.retries + 1):
            try:
                self.logger.info(
                    f"Reading Modbus registers | attempt={attempt} "
                    f"address={address} count={count}"
                )

                response = self.client.read_holding_registers(
                    address=address,
                    count=count,
                    slave=self.slave_id,
                )

                if response.isError():
                    raise Exception(response)

                return response.registers

            except Exception as e:
                self.logger.warning(
                    f"Read failed (attempt {attempt}): {e}"
                )
                time.sleep(0.2)

        self.logger.error("All retries failed")
        raise RuntimeError("Modbus read failed")

    def close(self):
        self.client.close()
        self.logger.info("Modbus connection closed")
