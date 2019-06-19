from states.states import StateMachine


class LemonatorInterface:
    def __init__(self, effectors, sensors):
        self.lcd = effectors['lcd']
        self.keypad = sensors['keypad']

        self.distance = sensors['level']
        self.colour = sensors['colour']
        self.temperature = sensors['temp']
        self.presence = sensors['presence']

        self.heater = effectors['heater']
        self.syrup_pump = effectors['pumpB']
        self.syrup_valve = effectors['valveB']
        self.water_pump = effectors['pumpA']
        self.water_valve = effectors['valveA']
        self.led_green = effectors['greenM']
        self.led_yellow = effectors['yellowM']

        # TODO: Define
        self.syrup = None
        self.water = None


def new_update(self) -> None:
    effectors = self._Controller__effectors
    sensors = self._Controller__sensors

    if not hasattr(self, "interface"):
        self.interface = LemonatorInterface(effectors, sensors)
        return
    if not hasattr(self, "stm"):
        self.stm = StateMachine(self.interface)
        return

    self.stm.update()


if __name__ == "__main__":
    """Only perform actions when invoked directly!"""
    from blackbox.Simulator import Simulator
    import types

    simulator = Simulator(True)  # use Simulator(False) to disable the GUI

    # Override the update function with our logic
    simulator._Simulator__controller.update = types.MethodType(
        new_update, simulator._Simulator__controller)

    # Start simulation
    simulator.run()
