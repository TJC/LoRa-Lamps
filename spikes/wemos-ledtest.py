import utime
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
LED_COUNT = 87
# Only 80 in second unit..
# Approx 25 in the "head" portion

pin = machine.Pin(LED_PIN, machine.Pin.OUT)
np = NeoPixel(pin, LED_COUNT)

offset = 0
while True:
    for i in range(LED_COUNT):
        hue = ((offset + i) % LED_COUNT) / 90
        np[i] = CHSVtoTuple8(fancyled.CHSV(hue))
    offset = (offset + 1) % LED_COUNT
    np.write()
    utime.sleep_ms(20)
