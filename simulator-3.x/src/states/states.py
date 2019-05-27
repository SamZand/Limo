from states.utills import Enum


class StateMachine:
    def __init__(self, interface):
        self.STATES = Enum("on", "pressure_build", "pour", "cancel", "keep_warm")
        self.on_state = OnState(self, interface)
        self.pressure_build_state = PressureBuildState(self, interface)
        self.pour_state = PourState(self, interface)
        self.cancel_state = CancelState(self, interface)
        self.keep_warm_state = KeepWarmState(self, interface)

        # Start at on_state
        self.state = self.on_state

    def __switch_state(self, new_state):
        self.state.reset()
        self.state = new_state
        self.state.on_enter()

    def switch_state(self, new_state):
        if new_state == self.STATES.ON:
            self.__switch_state(self.on_state)
        elif new_state == self.STATES.PRESSURE_BUILD:
            self.__switch_state(self.pressure_build_state)
        elif new_state == self.STATES.POUR:
            self.__switch_state(self.pour_state)
        elif new_state == self.STATES.CANCEL:
            self.__switch_state(self.cancel_state)
        elif new_state == self.STATES.KEEP_WARM:
            self.__switch_state(self.keep_warm_state)
        else:
            raise Exception("Unknown state")

    def update(self):
        self.state.update()


class State:
    def __init__(self, stm, interface):
        self.stm = stm
        self.interface = interface

    def on_enter(self):
        '''
        One iteration of the state

        :return: None
        '''
        raise Exception("Don't use abstract class")

    def update(self):
        '''
        One iteration of the state

        :return: None
        '''
        raise Exception("Don't use abstract class")

    def reset(self):
        '''
        Reset all effectors in the interface

        :return: None
        '''
        interface = self.interface
        # TODO: Does the lcd need a reset?
        # interface.lcd = effectors['lcd']

        interface.heater.switchOff()
        interface.syrup_pump.switchOff()
        interface.syrup_valve.switchOff()
        interface.water_pump.switchOff()
        interface.water_valve.switchOff()
        interface.led_green.switchOff()
        interface.led_yellow.switchOff()


class OnState(State):
    def __init__(self, stm, interface):
        super().__init__(stm, interface)

    def on_enter(self):
        self.interface.lcd.pushString('\fReady')

    def update(self):
        # No cup
        if not self.interface.presence.readValue():
            self.interface.lcd.pushString('\fNo cup')
        else:
            self.interface.lcd.pushString('\fReady')
            keypressed = self.interface.keypad.pop()
            if keypressed:
                print(keypressed)
                # Oke button pressed, go to next state
                if keypressed == 'A':
                    self.stm.switch_state(self.stm.STATES.PRESSURE_BUILD)

    def reset(self):
        super().reset()


class PressureBuildState(State):
    def __init__(self, stm, interface):
        super().__init__(stm, interface)
        # TODO: replace with time
        self.counter = 0
        self.pressure_time = 10

    def on_enter(self):
        self.interface.lcd.pushString('\fBuilding pressure...')
        self.counter = 0

    def update(self):
        # No cup, go to cancel state
        if not self.interface.presence.readValue():
            self.stm.switch_state(self.stm.STATES.CANCEL)

        self.counter += 1

        # We have pressure go to next state
        if self.counter == self.pressure_time:
            self.stm.switch_state(self.stm.STATES.POUR)

    def reset(self):
        super().reset()


class PourState(State):
    def __init__(self, stm, interface):
        super().__init__(stm, interface)

        self.cup_threshhold = 1

    def on_enter(self):
        self.interface.lcd.pushString('\fPouring...')

    def update(self):
        # Cup removed
        if not self.interface.presence.readValue():
            self.stm.switch_state(self.stm.STATES.CANCEL)
        # Cup full
        elif self.interface.distance.readValue() >= self.cup_threshhold:
            self.stm.switch_state(self.stm.STATES.KEEP_WARM)
        # Cup not full
        else:
            # TODO: Pumps only need to be turned on once
            # TODO: SETTINGS
            self.interface.water_pump.switchOn()
            self.interface.syrup_pump.switchOn()
            print(self.interface.distance.readValue())

    def reset(self):
        super().reset()


class CancelState(State):
    def __init__(self, stm, interface):
        super().__init__(stm, interface)

        # TODO: replace with time
        self.counter = 0
        self.wait_time = 60  # 2s

    def on_enter(self):
        self.interface.lcd.pushString('\fCANCELED')
        self.counter = 0

        # Open valves
        self.interface.water_valve.switchOn()
        self.interface.syrup_valve.switchOn()

    def update(self):
        self.counter += 1

        # Wait time has passed, go to next state
        if self.counter == self.wait_time:
            self.stm.switch_state(self.stm.STATES.ON)

    def reset(self):
        super().reset()


class KeepWarmState(State):
    def __init__(self, stm, interface):
        super().__init__(stm, interface)

    def on_enter(self):
        self.interface.lcd.pushString('\fKeeping warm')

        # Open valves
        self.interface.water_valve.switchOn()
        self.interface.syrup_valve.switchOn()

        # Turn on heater
        self.interface.heater.switchOn()

    def update(self):
        # Cup removed
        if not self.interface.presence.readValue():
            self.stm.switch_state(self.stm.STATES.ON)

    def reset(self):
        super().reset()
