import utime
import math
from machine import Pin
from neopixel import NeoPixel
from adafruit_fancyled import adafruit_fancyled as fancyled


def CHSVtoTuple8(hsv):
    """Returns a 3x8bit tuple, suitable for uPython neopixel library."""
    rgb = fancyled.CRGB(hsv)
    return (
        fancyled.denormalize(rgb.red),
        fancyled.denormalize(rgb.green),
        fancyled.denormalize(rgb.blue),
    )


LED_PIN = 6
LED_COUNT = 1

pin = machine.Pin(LED_PIN, machine.Pin.OUT)
np = NeoPixel(pin, LED_COUNT)

hue = 0.0
brighttrack = 0.0
while True:
    brightness = math.sin(brighttrack)
    np[0] = CHSVtoTuple8(fancyled.CHSV(hue, 1.0, brightness / 2))
    hue = hue + 0.001
    brighttrack = brighttrack + 0.01
    if hue > 1.0:
        hue = 0.0
    if brighttrack > 3.1415:
        brighttrack = 0.0
    np.write()
    utime.sleep_ms(20)
