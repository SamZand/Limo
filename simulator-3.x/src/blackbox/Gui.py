# uncompyle6 version 3.3.2
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\Gui.py
# Compiled at: 2018-03-14 09:19:04
# Size of source mod 2**32: 15735 bytes
import pygame
from pygame import *
from Constants import *
from Vessel import Vessel
from Effector import Heater, Led, LCD
from Sensor import Sensor
from time import sleep

class GUI:

    def __init__(self, plant=None, controller=None, monitor=None):
        self._GUI__plant = plant
        self._GUI__controller = controller
        self._GUI__monitor = monitor
        self._GUI__timestamp = 0
        self._GUI__run = False
        pygame.init()
        pygame.font.init()
        self._GUI__font = pygame.font.Font('blackbox/font/OpenSans-Regular.ttf', 12)
        self._GUI__monospace = pygame.font.Font('blackbox/font/LEDCalculator.ttf', 12)
        self._GUI__screen = pygame.display.set_mode(screensize)
        pygame.display.set_caption('Liquid Mixer Simulator GUI')
        pygame.mouse.set_visible(True)
        x, y = simPos
        w, h = (200, 100)
        self._GUI__icons = dict()
        self._GUI__icons['a'] = VesselIcon(self._GUI__screen, x, y, self._GUI__plant._vessels['a'])
        self._GUI__icons['b'] = VesselIcon(self._GUI__screen, x + w, y, self._GUI__plant._vessels['b'])
        self._GUI__icons['mix'] = VesselIcon(self._GUI__screen, x + w / 2, y + h - 15, self._GUI__plant._vessels['mix'])
        self._GUI__icons['heater'] = HeaterIcon(self._GUI__screen, x + w / 2, y + h + 45, self._GUI__plant._effectors['heater'])
        self._GUI__icons['temp'] = SensorIcon(self._GUI__screen, x + w, y + h * 3 / 4, self._GUI__plant._sensors['temp'], 'Temperature')
        self._GUI__icons['level'] = SensorIcon(self._GUI__screen, x + w, y + h * 3 / 4 + 25, self._GUI__plant._sensors['level'], 'Level')
        self._GUI__icons['color'] = SensorIcon(self._GUI__screen, x + w, y + h * 3 / 4 + 50, self._GUI__plant._sensors['colour'], 'Colour')
        self._GUI__icons['redA'] = LedIcon(self._GUI__screen, x + 60, y, self._GUI__plant._effectors['redA'])
        self._GUI__icons['greenA'] = LedIcon(self._GUI__screen, x + 60, y + 10, self._GUI__plant._effectors['greenA'])
        self._GUI__icons['redB'] = LedIcon(self._GUI__screen, x + w + 60, y, self._GUI__plant._effectors['redB'])
        self._GUI__icons['greenB'] = LedIcon(self._GUI__screen, x + w + 60, y + 10, self._GUI__plant._effectors['greenA'])
        self._GUI__icons['greenM'] = LedIcon(self._GUI__screen, x + w / 2 + 60, y + h - 15, self._GUI__plant._effectors['greenM'])
        self._GUI__icons['yellowM'] = LedIcon(self._GUI__screen, x + w / 2 + 60, y + h - 5, self._GUI__plant._effectors['yellowM'])
        self.step()

    def drawPipes(self) -> None:
        x, y = simPos
        w, h = (250, 100)
        pygame.draw.lines(self._GUI__screen, BLACK, False, [
         (
          x + 35, y + 5), (x + 35, y - 15), (x + w / 2 - 5, y - 15), (x + w / 2 - 5, y + h - 10)], 5)
        pygame.draw.lines(self._GUI__screen, BLACK, False, [
         (
          x + w - 35, y + 5), (x + w - 35, y - 15), (x + w / 2 + 5, y - 15), (x + w / 2 + 5, y + h - 10)], 5)

    def drawButtons(self, x: int=buttonPos[0],
                    y: int=buttonPos[1]) -> None:
        """
        Draws the button panel
        """
        x1 = x + buttonWidth / 2 + 5
        halfWidth = buttonWidth / 2 - 5
        pygame.draw.rect(self._GUI__screen, ORANGE, [x, y, halfWidth, buttonHeight])
        if self._GUI__run:
            pygame.draw.rect(self._GUI__screen, WHITE, [x + 17, y + 5, 10, 20])
            pygame.draw.rect(self._GUI__screen, WHITE, [x + 32, y + 5, 10, 20])
        else:
            pygame.draw.polygon(self._GUI__screen, WHITE, [(x + 27, y + 5), (x + 27, y + 25), (x + 43, y + 15)])
        pygame.draw.rect(self._GUI__screen, ORANGE, [x1, y, halfWidth, buttonHeight])
        pygame.draw.polygon(self._GUI__screen, WHITE, [(x1 + 15, y + 5), (x1 + 15, y + 25), (x1 + 30, y + 15)])
        pygame.draw.rect(self._GUI__screen, WHITE, [x1 + 35, y + 5, 10, 20])
        y += buttonHeight + margin / 2
        pygame.draw.rect(self._GUI__screen, ORANGE, [x, y, halfWidth, buttonHeight])
        pumpA = 'Pump A'
        label = self._GUI__font.render(pumpA, False, RED if self._GUI__plant._effectors['pumpA'].isOn() else WHITE)
        w, h = self._GUI__font.size(pumpA)
        self._GUI__screen.blit(label, [x + w / 2, y + h / 2])
        pygame.draw.rect(self._GUI__screen, ORANGE, [x1, y, halfWidth, buttonHeight])
        pumpA = 'Valve A'
        label = self._GUI__font.render(pumpA, False, RED if self._GUI__plant._effectors['valveA'].isOn() else WHITE)
        w, h = self._GUI__font.size(pumpA)
        self._GUI__screen.blit(label, [x1 + w / 2, y + h / 2])
        y += buttonHeight + margin / 2
        pygame.draw.rect(self._GUI__screen, ORANGE, [x, y, halfWidth, buttonHeight])
        pumpB = 'Pump B'
        label = self._GUI__font.render(pumpB, False, RED if self._GUI__plant._effectors['pumpB'].isOn() else WHITE)
        w, h = self._GUI__font.size(pumpB)
        self._GUI__screen.blit(label, [x + w / 2, y + h / 2])
        pygame.draw.rect(self._GUI__screen, ORANGE, [x1, y, halfWidth, buttonHeight])
        pumpB = 'Valve B'
        label = self._GUI__font.render(pumpB, False, RED if self._GUI__plant._effectors['valveB'].isOn() else WHITE)
        w, h = self._GUI__font.size(pumpB)
        self._GUI__screen.blit(label, [x1 + w / 2, y + h / 2])
        y += buttonHeight + margin / 2
        pygame.draw.rect(self._GUI__screen, ORANGE, [x, y, buttonWidth, buttonHeight])
        heater = 'Heater: ' + ('on ' if self._GUI__plant._effectors['heater'].isOn() else 'off')
        label = self._GUI__font.render(heater, False, RED if self._GUI__plant._effectors['heater'].isOn() else WHITE)
        w, h = self._GUI__font.size(heater)
        self._GUI__screen.blit(label, [x + w / 2, y + h / 2])
        y += buttonHeight + margin / 2
        pygame.draw.rect(self._GUI__screen, ORANGE, [x, y, buttonWidth, buttonHeight])
        cup = 'Cup: ' + ('present' if self._GUI__plant._vessels['mix'].getPresence() else 'away')
        label = self._GUI__font.render(cup, False, RED if self._GUI__plant._vessels['mix'].getPresence() else WHITE)
        w, h = self._GUI__font.size(cup)
        self._GUI__screen.blit(label, [x + w / 2, y + h / 2])

    def drawGraph(self, x: int=30,
                  y: int=240, w: int=170, h: int=140, maxVal: float=3.3, resource: str='temp', colour=RED):
        """Draws a graph of the given resource on location (x,y) (upper left corner) with width w and height h"""
        if resource in self._GUI__monitor._effectorValues:
            maxVal = 1
        if resource == 'level':
            scale = h / maxVal * (maxVal / (2 * eval(resource + 'SetPoint')))
        else:
            scale = h / maxVal
        pygame.draw.lines(self._GUI__screen, BLACK, False, [(x, y), (x, y + h), (x + w, y + h)])
        label = self._GUI__font.render('0', False, BLACK)
        tw, th = self._GUI__font.size('0')
        self._GUI__screen.blit(label, [x - tw - 5, y + h])
        label = self._GUI__font.render(str(maxVal), False, BLACK)
        tw, th = self._GUI__font.size(str(maxVal))
        self._GUI__screen.blit(label, [x - tw - 5, y - th])
        x0, y0 = x, y + h
        if resource in self._GUI__monitor._sensorReadings:
            data = self._GUI__monitor._sensorReadings[resource][-w:]
            setPoint = eval(resource + 'SetPoint')
            pygame.draw.line(self._GUI__screen, ORANGE, [x0, y0 - setPoint * scale], [x0 + w, y0 - setPoint * scale])
            label = self._GUI__font.render(str(setPoint), False, ORANGE)
            tw, th = self._GUI__font.size(str(setPoint))
            self._GUI__screen.blit(label, [x - tw, y0 - th / 2 - setPoint * scale])
        else:
            if resource in self._GUI__monitor._effectorValues:
                data = self._GUI__monitor._effectorValues[resource][-w:]
        if len(data) < w:
            px, py = x0, y0
        else:
            px, py = x0, y0 - data[0] * scale
        for reading in data:
            prevX, prevY = px, py
            px += 1
            py = y0 - reading * scale
            pygame.draw.line(self._GUI__screen, colour, [prevX, prevY], [px, py], 2)

        label = self._GUI__font.render(resource.title(), False, BLACK)
        tw, th = self._GUI__font.size(resource.title())
        self._GUI__screen.blit(label, [x + w / 2 - tw / 2, y - th])

    def drawGraphs(self) -> None:
        for resource in graphs.keys():
            x, y, w, h, c = graphs[resource]
            self.drawGraph(x, y, w, h, resource=resource, colour=c)

    def drawKeypad(self, x: int=simPos[0] + 450, y: int=simPos[1] + 25) -> None:
        xPos, yPos = x, y
        w, h = (35, 35)
        m = 10
        for key in ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']:
            pygame.draw.rect(self._GUI__screen, ORANGE if key.isdigit() else RED, [xPos, yPos, w, h])
            pygame.draw.rect(self._GUI__screen, WHITE, [xPos + 1, yPos + 1, w - 2, h - 2], 1)
            label = self._GUI__font.render(key, False, WHITE)
            tw, th = self._GUI__font.size(key)
            self._GUI__screen.blit(label, [xPos + w / 2 - tw / 2, yPos + h / 2 - th / 2])
            xPos = x if key.isalpha() else xPos + m + w
            yPos = yPos + m + h if key.isalpha() else yPos

    def drawLCD(self, x: int=simPos[0] + 455, y: int=simPos[1] - 50, w: int=160, h: int=60, lcd: LCD=None) -> None:
        pygame.draw.rect(self._GUI__screen, GREEN, [x, y, w, h])
        yPos = y + 2
        for line in lcd.getLines():
            label = self._GUI__monospace.render(line[:20], False, BLACK)
            self._GUI__screen.blit(label, [x + 7, yPos])
            yPos += 13

    def update(self) -> None:
        self._GUI__screen.fill((250, 250, 250))
        for icon in self._GUI__icons.values():
            icon.draw()

        self.drawPipes()
        self.drawButtons()
        self.drawGraphs()
        self.drawKeypad()
        self.drawLCD(lcd=self._GUI__plant._effectors['lcd'])
        label = self._GUI__font.render(str(self._GUI__timestamp), True, BLACK)
        self._GUI__screen.blit(label, [margin, margin])
        pygame.display.update()

    def step(self) -> None:
        self._GUI__timestamp += 1
        self._GUI__plant.update()
        self._GUI__controller.update()
        self._GUI__monitor.update()

    def run(self) -> None:
        while True:
            if self._GUI__run:
                self.step()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if buttonPos[0] < pos[0] <= buttonPos[0] + buttonWidth:
                        if buttonPos[1] < pos[1] <= buttonPos[1] + buttonHeight and pos[0] < buttonPos[0] + buttonWidth / 2:
                            self._GUI__run = False if self._GUI__run else True
                        else:
                            if buttonPos[1] < pos[1] <= buttonPos[1] + buttonHeight and pos[0] > buttonPos[0] + buttonWidth / 2:
                                if not self._GUI__run:
                                    self.step()
                            else:
                                if buttonPos[1] + 1 * (buttonHeight + margin / 2) < pos[1] <= buttonPos[1] + 1 * (buttonHeight + margin / 2) + buttonHeight:
                                    if pos[0] < buttonPos[0] + buttonWidth / 2:
                                        self._GUI__plant._effectors['pumpA'].switchOff() if self._GUI__plant._effectors['pumpA'].isOn() else self._GUI__plant._effectors['pumpA'].switchOn()
                                    else:
                                        if pos[0] > buttonPos[0] + buttonWidth / 2:
                                            self._GUI__plant._effectors['valveA'].switchOff() if self._GUI__plant._effectors['valveA'].isOn() else self._GUI__plant._effectors['valveA'].switchOn()
                                else:
                                    if buttonPos[1] + 2 * (buttonHeight + margin / 2) < pos[1] <= buttonPos[1] + 2 * (buttonHeight + margin / 2) + buttonHeight:
                                        if pos[0] < buttonPos[0] + buttonWidth / 2:
                                            self._GUI__plant._effectors['pumpB'].switchOff() if self._GUI__plant._effectors['pumpB'].isOn() else self._GUI__plant._effectors['pumpB'].switchOn()
                                        else:
                                            if pos[0] > buttonPos[0] + buttonWidth / 2:
                                                self._GUI__plant._effectors['valveB'].switchOff() if self._GUI__plant._effectors['valveB'].isOn() else self._GUI__plant._effectors['valveB'].switchOn()
                                    else:
                                        if buttonPos[1] + 3 * (buttonHeight + margin / 2) < pos[1] <= buttonPos[1] + 3 * (buttonHeight + margin / 2) + buttonHeight:
                                            self._GUI__plant._effectors['heater'].switchOff() if self._GUI__plant._effectors['heater'].isOn() else self._GUI__plant._effectors['heater'].switchOn()
                                        else:
                                            if buttonPos[1] + 4 * (buttonHeight + margin / 2) < pos[1] <= buttonPos[1] + 4 * (buttonHeight + margin / 2) + buttonHeight:
                                                self._GUI__plant._vessels['mix'].setPresence()
                    keypadPos = (
                     simPos[0] + 450, simPos[1] + 25)
                    kpw, kph, kpm = (35, 35, 10)
                    if keypadPos[0] < pos[0] <= keypadPos[0] + 170:
                        keys = [
                         '1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*', '0', '#', 'D']
                        index = int((pos[0] - keypadPos[0]) // 42.5 + (pos[1] - keypadPos[1]) // 42.5 * 4)
                        self._GUI__plant._sensors['keypad'].push(keys[index])

            self.update()
            sleep(0.25)


class Icon:

    def __init__(self, screen: 0, x: int=0, y: int=0):
        self._x = int(x)
        self._y = int(y)
        self._screen = screen
        self._font = pygame.font.Font('blackbox/font/OpenSans-Regular.ttf', 12)

    def draw(self) -> None:
        text = self._font.render('?', False, BLACK)
        self._screen.blit(text, [self._x, self._y])


class VesselIcon(Icon):

    def __init__(self, screen: pygame.display,
                 x: int, y: int, vessel: Vessel) -> None:
        Icon.__init__(self, screen, x, y)
        self._vessel = vessel

    def draw(self) -> None:
        colour = self._vessel.getColour()
        level = self._vessel.getFluidAmount() / liquidMax * 100
        pygame.draw.rect(self._screen, (colour * 2.55, 0, 255 - colour * 2.55), [self._x, self._y + 51 - level * 0.4, 50, level * 0.4])
        pygame.draw.lines(self._screen, BLACK, False, [(self._x, self._y), (self._x, self._y + 50), (self._x + 50, self._y + 50), (self._x + 50, self._y)], 2)


class HeaterIcon(Icon):

    def __init__(self, screen: pygame.display,
                 x: int, y: int, heater: Heater) -> None:
        Icon.__init__(self, screen, x, y)
        self._heater = heater

    def draw(self) -> None:
        pygame.draw.line(self._screen, BLACK, [self._x, self._y], [self._x + 50, self._y], 4)
        if self._heater.isOn():
            x = self._x + 2
            for i in range(6):
                pygame.draw.lines(self._screen, (0, 0, 0), True, [(x, self._y - 2), (x + 3, self._y - 6), (x + 6, self._y - 2)], 2)
                x += 8


class SensorIcon(Icon):

    def __init__(self, screen: pygame.display,
                 x: int, y: int, sensor: Sensor, name: str) -> None:
        Icon.__init__(self, screen, x, y)
        self._name = name
        self._sensor = sensor

    def draw(self) -> None:
        name = self._name + ':'
        value = str(self._sensor.readValue()) + ' / ' + self._sensor.measure()
        nameLabel = self._font.render(name, False, BLACK)
        self._screen.blit(nameLabel, [self._x, self._y])
        valueLabel = self._font.render(value, False, BLACK)
        self._screen.blit(valueLabel, [self._x + 85, self._y])


class LedIcon(Icon):

    def __init__(self, screen: pygame.display,
                 x: int, y: int, led: Led) -> None:
        Icon.__init__(self, screen, x, y)
        self._led = led

    def draw(self) -> None:
        colour = self._led.getColour()
        if self._led.isOn():
            pygame.draw.circle(self._screen, colour, [self._x, self._y], 5)
        else:
            pygame.draw.circle(self._screen, (int(colour[0] / 3), int(colour[1] / 3), int(colour[2] / 3)), [self._x, self._y], 5)
        pygame.draw.circle(self._screen, BLACK, [self._x, self._y], 5, 1)
# okay decompiling Gui.pyc
