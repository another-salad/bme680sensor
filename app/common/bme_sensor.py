"""BME 680 Sensor"""

import board
from  adafruit_bme680 import Adafruit_BME680_I2C

from config_reader import get_conf


class BMESensor(Adafruit_BME680_I2C):
    """BME Sensor wrapper"""

    def __init__(self, i2c=board.I2C(), sea_level_pressure=get_conf()):
        """init baby"""
        super().__init__(i2c=i2c)
        self.sea_level_pressure = sea_level_pressure.seaLevelhPa
