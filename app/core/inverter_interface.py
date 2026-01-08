from abc import ABC, abstractmethod


class InverterInterface(ABC):

    @abstractmethod
    def read_registers(self, address: int, count: int):
        pass
