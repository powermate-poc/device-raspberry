import math
from abc import ABC
from smbus2 import SMBus


class MagnetSensor(ABC):
    def read(self) -> tuple[float, float, float, float]:
        return 0, 0, 0, 0


class RealMagnetSensor(MagnetSensor):
    bus_num: int
    address: int
    bus: SMBus

    def __init__(self, bus_num: int = 1, address: int = 0x0d) -> None:
        self.bus_num = bus_num
        self.address = address

        self.bus = SMBus(bus_num)

        # Write to the sensor to enable continuous measurement mode
        self.bus.write_byte_data(address, 0x0B, 0x01)
        self.bus.write_byte_data(address, 0x09, 0x01 | 0x0C | 0x10 | 0X00)

    def read(self) -> tuple[float, float, float, float]:
        self.bus.write_byte(self.address, 0x0)
        data = self.bus.read_i2c_block_data(
            i2c_addr=self.address, register=0x0, length=6)

        magnet_x = (data[0]) | ((data[1]) << 8)
        if magnet_x > 32767:
            magnet_x -= 65536
        magnet_y = (data[2]) | ((data[3]) << 8)
        if magnet_y > 32767:
            magnet_y -= 65536
        magnet_z = (data[4]) | ((data[5]) << 8)
        if magnet_z > 32767:
            magnet_z -= 65536
        absolute = math.sqrt(magnet_x**2 + magnet_y**2 + magnet_z**2)
        return magnet_x, magnet_y, magnet_z, absolute
