from machine import ADC, Pin
from neopixel import NeoPixel
import utime

LED_PIN = 15  # 16 Lolin Wemos S2. Is pin 6 on the C3. 15 on tinypico
LED_COUNT = 50
ADC_PIN = 33  # 33 on Tinypico. 5 on Wemos s2 and c3.
DC_OFFSET = const(1255000)

pin = Pin(LED_PIN, Pin.OUT)
np = NeoPixel(pin, LED_COUNT)
adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)

# Works well with windowSize=600, q=3
# Seems to beat-detect well at 100,1.7 too


# Try to get the max absolute value, over a 20ms period
def getMaxRead():
    maxval = 0
    for i in range(0, 40):
        v = abs(adc.read_uv() - DC_OFFSET)
        if v > maxval:
            maxval = v
        utime.sleep_us(500)
    return maxval


# This is now working well with t(50, 1.25, 1)
def t(windowSize, q, delay):
    rollingAvg = 0
    maxInput = (
        2250000 / 2
    )  # 2250000 is claimed spec; dividing by two as don't seem to see it in practice
    ledValDivisor = maxInput / (LED_COUNT - 5)
    while True:
        v = getMaxRead()
        rollingAvg -= rollingAvg / windowSize
        rollingAvg += v / windowSize
        np.fill((0, 0, 0))

        # Show the average level
        ledCount = min(LED_COUNT - 5, int(rollingAvg / ledValDivisor))
        for i in range(0, ledCount):
            np[i] = (32, 0, 0)

        # Show the peak level
        peak = min(LED_COUNT - 5, int(v / ledValDivisor))
        np[peak] = (64, 64, 64)

        if v > q * rollingAvg:
            for i in range(LED_COUNT - 5, LED_COUNT):
                np[i] = (0, 64, 0)

        np.write()
        utime.sleep_ms(delay)
