def new_update(self) -> None:
    # TODO: Replace with interface
    effectors = self._Controller__effectors
    sensors = self._Controller__sensors

    # No cup, disable everything
    if not sensors['presence'].readValue():
        effectors['greenM'].switchOff()
        if effectors['heater'].isOn() or effectors['pumpA'].isOn() or effectors['pumpB'].isOn():
            print('No cup placed; stopping all')
        effectors['heater'].switchOff()
        effectors['yellowM'].switchOff()
        effectors['pumpA'].switchOff()
        effectors['redA'].switchOff()
        effectors['valveA'].switchOn()
        effectors['greenA'].switchOn()
        effectors['redB'].switchOff()
        effectors['pumpB'].switchOff()
        effectors['valveB'].switchOn()
        effectors['greenB'].switchOn()
        return


    keypressed = sensors['keypad'].pop()
    # TODO: HUIB? if keypressed werkt toch ook?
    if not keypressed == '\x00':
        print('Keypress detected!')

        if keypressed == 'A':
            print('Received an A')
            if effectors['pumpA'].isOn():
                effectors['pumpA'].switchOff()
                effectors['lcd'].pushString('\fPump A turned off!')
            else:
                effectors['pumpA'].switchOn()
                effectors['lcd'].pushString('\fPump A turned on!')

            effectors['greenA'].switchOn()
        if keypressed == 'B':
            print('Received an B')
            if effectors['pumpB'].isOn():
                effectors['pumpB'].switchOff()
                effectors['lcd'].pushString('\fPump B turned off!')
            else:
                effectors['pumpB'].switchOn()
                effectors['lcd'].pushString('\fPump B turned on!')

    self.test = 10
    print("Het", self.test)

if __name__ == "__main__":
    """Only perform actions when invoked directly!"""
    from blackbox.Simulator import Simulator
    import types

    simulator = Simulator(True)  # use Simulator(False) to disable the GUI

    # Override the update function with our logic
    simulator._Simulator__controller.update = types.MethodType(new_update, simulator._Simulator__controller)


    # Start simulation
    simulator.run()
