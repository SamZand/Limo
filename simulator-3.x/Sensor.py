# uncompyle6 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\Sensor.py
# Size of source mod 2**32: 2417 bytes
from Vessel import Vessel
from math import pi
from Constants import *

class Sensor:

    def __init__(self, vessel):
        self._vessel = vessel
        self._value = 0
        self._unitOfMeasure = ''

    def update(self) -> None:
        pass

    def readValue(self) -> float:
        return round(self._value, 2)

    def measure(self) -> str:
        return str(self._convertToValue()) + self._unitOfMeasure

    def _convertToValue(self) -> float:
        return round(self._value, 2)


class ColourSensor(Sensor):

    def __init__(self, vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = '%'

    def update(self) -> None:
        if type(self._vessel) != None:
            colour = self._vessel.getColour()
            self._value = colour * colourConversion

    def _convertToValue(self) -> float:
        return round(self._value / colourConversion, 2)


class TemperatureSensor(Sensor):

    def __init__(self, vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = '°C'

    def update(self) -> None:
        if type(self._vessel) != None:
            temperature = self._vessel.getTemperature()
            self._value = temperature * tempConversion

    def _convertToValue(self) -> float:
        return round(self._value / tempConversion, 2)


class LevelSensor(Sensor):

    def __init__(self, vessel):
        Sensor.__init__(self, vessel)
        self._unitOfMeasure = 'ml'

    def update(self) -> None:
        if type(self._vessel) != None:
            level = self._vessel.getFluidAmount()
            height = level / pi / 10 / 10
            self._value = height * levelConversion

    def _convertToValue(self) -> float:
        return round(self._value / levelConversion * pi * 10 * 10, 2)


class PresenceSensor(Sensor):

    def update(self) -> None:
        if type(self._vessel) != None:
            self._value = self._vessel.getPresence()

    def readValue(self) -> bool:
        return self._value

    def _convertToValue(self) -> bool:
        return self._value


class KeyPad(Sensor):

    def __init__(self):
        Sensor.__init__(self, None)
        self._keysPressed = []

    def push(self, c) -> None:
        self._keysPressed.append(c)

    def pop(self) -> str:
        if len(self._keysPressed) > 0:
            return self._keysPressed.pop(0)
        else:
            return '\x00'
# okay decompiling Sensor.pyc
