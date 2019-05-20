# uncompyle6 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: .\Simulator.py
# Size of source mod 2**32: 3765 bytes
from Controller import Controller
from Vessel import Vessel, MixtureVessel
from Sensor import *
from Effector import *
from Constants import *
from Gui import GUI
from typing import Dict
import time

class Plant:

    def __init__(self):
        self._vessels = {'mix': MixtureVessel(amount=100, temperature=36, colour=50)}
        self._vessels['a'] = Vessel(colour=0, amount=liquidMax, flowTo=self._vessels['mix'])
        self._vessels['b'] = Vessel(colour=100, amount=liquidMax, flowTo=self._vessels['mix'])
        self._sensors = {'colour':ColourSensor(self._vessels['mix']), 
         'temp':TemperatureSensor(self._vessels['mix']), 
         'level':LevelSensor(self._vessels['mix']), 
         'presence':PresenceSensor(self._vessels['mix']), 
         'keypad':KeyPad()}
        self._effectors = {'heater':Heater(self._vessels['mix']), 
         'pumpA':Pump(self._vessels['a']), 
         'valveA':Valve(self._vessels['a']), 
         'pumpB':Pump(self._vessels['b']), 
         'valveB':Valve(self._vessels['b']), 
         'redA':Led(RED), 
         'greenA':Led(GREEN), 
         'redB':Led(RED), 
         'greenB':Led(GREEN), 
         'greenM':Led(GREEN), 
         'yellowM':Led(YELLOW), 
         'lcd':LCD()}
        self._effectors['valveA'].setPump(self._effectors['pumpA'])
        self._effectors['valveB'].setPump(self._effectors['pumpB'])

    def update(self) -> None:
        for vessel in self._vessels.values():
            vessel.update()

        for sensor in self._sensors.values():
            sensor.update()

        for effector in self._effectors.values():
            effector.update()

    def printState(self) -> None:
        for sensor in self._sensors.values():
            print('type:', type(sensor), 'value:', sensor.readValue(), '->', sensor.measure())

        for effector in self._effectors.values():
            print('type:', type(effector), 'value:', 'on' if effector.isOn() else 'off')


class Simulator:

    def __init__(self, gui=False):
        self._Simulator__plant = Plant()
        self._Simulator__controller = Controller(self._Simulator__plant._sensors, self._Simulator__plant._effectors)
        self._Simulator__monitor = Monitor(self._Simulator__plant._sensors, self._Simulator__plant._effectors)
        if gui:
            self._Simulator__gui = GUI(self._Simulator__plant, self._Simulator__controller, self._Simulator__monitor)
        else:
            self._Simulator__gui = None

    def run(self) -> None:
        if self._Simulator__gui is None:
            timestamp = 0
            while True:
                timestamp += 1
                time.sleep(1)
                print(timestamp, '----------------------------------------')
                self._Simulator__plant.update()
                self._Simulator__controller.update()
                self._Simulator__monitor.update()
                self._Simulator__plant.printState()

        else:
            self._Simulator__gui.run()


class Monitor:

    def __init__(self, sensors, effectors):
        self._Monitor__sensors = sensors
        self._Monitor__effectors = effectors
        self._sensorReadings = {}
        self._effectorValues = {}
        for sensor in self._Monitor__sensors:
            self._sensorReadings[sensor] = []

        for effector in self._Monitor__effectors:
            self._effectorValues[effector] = []

    def update(self) -> None:
        for sensor in self._Monitor__sensors:
            self._sensorReadings[sensor].append(self._Monitor__sensors[sensor].readValue())

        for effector in self._Monitor__effectors:
            self._effectorValues[effector].append(self._Monitor__effectors[effector].isOn())


if __name__ == '__main__':
    simulator = Simulator(True)
    simulator.run()
# okay decompiling Simulator.pyc
