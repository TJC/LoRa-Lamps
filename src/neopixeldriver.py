import uasyncio as asyncio
from machine import Pin
from neopixel import NeoPixel
from adafruit_fancyled import adafruit_fancyled as fancyled
import os


class NeopixelDriver:
    LED_COUNT = 87
    leds: NeoPixel = None

    def init():
        if os.uname().machine.startswith("LOLIN_C3_MINI"):
            ledPin = Pin(6, Pin.OUT)
        elif os.uname().machine.startswith("LILYGO TTGO LoRa32"):
            ledPin = Pin(15, Pin.OUT)  # undecided
        elif os.uname().machine.startswith("TinyPICO with ESP32-PICO-D4"):
            # undecided, could be 15 or 14 or 27
            ledPin = Pin(15, Pin.OUT)
        NeopixelDriver.leds = NeoPixel(ledPin, NeopixelDriver.LED_COUNT)

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

    def CHSVtoTuple8(hsv):
        """Returns a 3x8bit tuple, suitable for uPython neopixel library."""
        rgb = fancyled.CRGB(hsv)
        return (
            fancyled.denormalize(rgb.red),
            fancyled.denormalize(rgb.green),
            fancyled.denormalize(rgb.blue),
        )
