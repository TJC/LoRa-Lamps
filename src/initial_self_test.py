import utime
from boards import Boards
from machine import Pin
from neopixel import NeoPixel


# Run a boot-up sequence that turns on all the lights as a self-test
class InitialSelfTest:
    def __init__(self):
        self.boardInfo = Boards.metadata()

    def run(self):
        self.tripleBlink()
        self.neopixelTest()

    def toggleInternalLed(self):
        if self.boardInfo["internalLedPin"] == None:
            return
        pin = Pin(self.boardInfo["internalLedPin"], Pin.OUT)
        pin.value((pin.value() + 1) % 2)

    def tripleBlink(self):
        for i in range(0, 6):
            self.toggleInternalLed()
            utime.sleep(0.33)

    # Display red, green, blue, white, then blank
    def neopixelTest(self):
        if self.boardInfo["extLedPin"] == None:
            return
        pin = Pin(self.boardInfo["extLedPin"], Pin.OUT)
        leds = NeoPixel(pin, self.boardInfo["ledCount"])

        tuples = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)]
        for col in tuples:
            leds.fill(col)
            leds.write()
            utime.sleep_ms(500)
