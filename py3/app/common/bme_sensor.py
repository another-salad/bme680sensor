"""BME 680 Sensor"""

import board
from  adafruit_bme680 import Adafruit_BME680_I2C

from config_reader import get_conf


# BME Sensor object
class BMESensor(Adafruit_BME680_I2C):
    """BME Sensor wrapper"""

    def __init__(self, i2c=board.I2C(), sea_level_pressure=get_conf()):
        """init baby"""
        super().__init__(i2c=i2c)
        self.sea_level_pressure = sea_level_pressure.seaLevelhPa


# BME680 Sensor data
class BMESensorProperties(BMESensor):
    """Gets the sensor data for the socket emits"""

    def __init__(self, sea_level_pressure):
        """init baby"""
        super().__init__(sea_level_pressure=sea_level_pressure)

    @property
    def getTemp(self) -> tuple:
        """get temp"""
        return 'getTemp', round(self.temperature, 2)

    @property
    def getHumidity(self) -> tuple:
        """get humidity"""
        return 'getHumidity', round(self.humidity, 2)

    @property
    def getAirQuality(self) -> tuple:
        """get AirQuality"""
        return 'getAirQuality', self.gas

    @property
    def getPressure(self) -> tuple:
        """get pressure"""
        return 'getPressure', round(self.pressure, 2)
