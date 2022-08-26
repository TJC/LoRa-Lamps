import uasyncio as asyncio
from machine import Pin
from neopixel import NeoPixel
from adafruit_fancyled import adafruit_fancyled as fancyled
import os
import random


class NeopixelDriver:
    LED_COUNT = 87
    leds: NeoPixel = None
    effectLeds: list[tuple[int, int, int]] = [(0, 0, 0)] * LED_COUNT
    trigger: asyncio.Event = None

    def init():
        if os.uname().machine.startswith("LOLIN_C3_MINI"):
            ledPin = Pin(6, Pin.OUT)
        elif os.uname().machine.startswith("LILYGO TTGO LoRa32"):
            ledPin = Pin(15, Pin.OUT)  # undecided
        elif os.uname().machine.startswith("TinyPICO with ESP32-PICO-D4"):
            # undecided, could be 15 or 14 or 27
            ledPin = Pin(15, Pin.OUT)
        NeopixelDriver.leds = NeoPixel(ledPin, NeopixelDriver.LED_COUNT)
        NeopixelDriver.trigger = asyncio.Event()

    async def mainLoop():
        while True:
            await NeopixelDriver.trigger.wait()
            NeopixelDriver.trigger.clear()

            # Integrate the other effects.. let's do this hackily for now:
            for i in range(0, NeopixelDriver.LED_COUNT):
                NeopixelDriver.leds[i] = NeopixelDriver.mergeWithClamp(
                    NeopixelDriver.leds[i], NeopixelDriver.effectLeds[i]
                )

            NeopixelDriver.leds.write()

    # A simple effect we can trigger to see if sensors work..
    async def pulseEffect():
        for i in range(0, 128):
            for j in range(55, NeopixelDriver.LED_COUNT):
                NeopixelDriver.effectLeds[j] = (i, i, i)
            await asyncio.sleep_ms(15)
        for i in range(128, 0, -1):
            for j in range(55, NeopixelDriver.LED_COUNT):
                NeopixelDriver.effectLeds[j] = (i, i, i)
            await asyncio.sleep_ms(15)
        for j in range(55, NeopixelDriver.LED_COUNT):
            NeopixelDriver.effectLeds[j] = (0, 0, 0)

    def blank():
        NeopixelDriver.leds.fill((0, 0, 0))
        NeopixelDriver.leds.write()

    async def rainbow_loop():
        offset = 0
        while True:
            for i in range(NeopixelDriver.LED_COUNT):
                hue = (
                    (offset + i) % NeopixelDriver.LED_COUNT
                ) / NeopixelDriver.LED_COUNT
                NeopixelDriver.leds[i] = NeopixelDriver.CHSVtoTuple8(fancyled.CHSV(hue))
            offset = (offset + 1) % NeopixelDriver.LED_COUNT
            NeopixelDriver.leds.write()
            asyncio.sleep_ms(20)

    def mergeWithClamp(a, b):
        r = min(255, a[0] + b[0])
        g = min(255, a[1] + b[1])
        b = min(255, a[2] + b[2])
        return (r, g, b)

    def CHSVtoTuple8(hsv):
        """Returns a 3x8bit tuple, suitable for uPython neopixel library."""
        rgb = fancyled.CRGB(hsv)
        return (
            fancyled.denormalize(rgb.red),
            fancyled.denormalize(rgb.green),
            fancyled.denormalize(rgb.blue),
        )

    # input should be 0-255
    def heatColour(temp256: int):
        heatramp = 3 * (temp256 % 86)  # heatramp at most 255
        if temp256 < 86:  # coolest third
            return (heatramp, 0, 0)  # ramp up red, no green or blue
        elif temp256 < 171:
            return (255, heatramp, 0)  # full red, ramp up green, no blue yet
        else:
            return (255, 255, heatramp)  # full red & green, ramp up blue

    # Modified version of the original Fire2012 algorithm from FastLED
    async def fire2022():
        random.seed()

        # Suggested range 20-100. Default 55
        COOLING = 55
        COOLING_FACTOR = int(10 * COOLING / NeopixelDriver.LED_COUNT) + 2
        SPARKING_FACTOR = 0.28

        cells = [0] * NeopixelDriver.LED_COUNT

        while True:
            # Step 1, cool down every cell a little
            for i in range(0, NeopixelDriver.LED_COUNT):
                cells[i] = cells[i] - random.randint(0, COOLING_FACTOR)
                if cells[i] < 0:
                    cells[i] = 0

            # Step 2, Heat from each cell drifts up and diffuses a little
            for i in range(NeopixelDriver.LED_COUNT - 1, 1, -1):
                cells[i] = int((cells[i - 1] + cells[i - 2] + cells[i - 2]) / 3)

            # Step 3, randomly ignite new sparks of heat near the bottom
            if random.random() < SPARKING_FACTOR:
                i = random.randint(0, 8)
                cells[i] = cells[i] + random.randint(160, 250)
                if cells[i] > 255:
                    cells[i] = 255

            # Step 4, map from heat cells to LED colours
            for i in range(0, NeopixelDriver.LED_COUNT):
                NeopixelDriver.leds[i] = NeopixelDriver.heatColour(cells[i])

            # Finally, write out the pixels and then delay
            NeopixelDriver.trigger.set()
            await asyncio.sleep_ms(33)


# from neopixeldriver import NeopixelDriver
# NeopixelDriver.init()
# import uasyncio
# uasyncio.run(NeopixelDriver.fire2022())
