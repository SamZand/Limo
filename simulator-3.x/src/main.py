from states.states import StateMachine

import time

import lemonator

lemonator.openInterface(4, True, True)

class LemonatorInterface:
    def __init__(self, effectors, sensors):
        self.lcd = lemonator.getLCD()
        self.keypad = lemonator.getKeyPad()

        self.distance = lemonator.getDistance()
        self.colour = lemonator.getColour()
        self.temperature = lemonator.getTemperature()
        self.presence = lemonator.getPresence()

        self.heater = lemonator.getHeater()
        self.syrup_pump = lemonator.getSyrupPump()
        self.syrup_valve = lemonator.getSyrupValve()
        self.water_pump = lemonator.getWaterPump()
        self.water_valve = lemonator.getWaterValve()
        self.led_green = lemonator.getLedGreen()
        self.led_yellow = lemonator.getLedYellow()

        # TODO: Define
        self.syrup = None
        self.water = None


class Plant:
    def __init__(self):
        self.interface = LemonatorInterface(None, None)
        self.stm = StateMachine(self.interface)


if __name__ == "__main__":
    p = Plant()

    """Only perform actions when invoked directly!"""
    
    timestamp = 0
    while True:
        timestamp += 1
        time.sleep(1)
        p.stm.update()

    # from blackbox.Simulator import Simulator
    # import types

    # simulator = Simulator(False)  # use Simulator(False) to disable the GUI

    # # Override the update function with our logic
    # simulator._Simulator__controller.update = types.MethodType(
    #     new_update, simulator._Simulator__controller)

    # # Start simulation
    # simulator.run()
