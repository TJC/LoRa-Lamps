from machine import ADC, Pin
from neopixel import NeoPixel
import utime
import uasyncio as asyncio

LED_PIN = 15  # 16 Lolin Wemos S2. Is pin 6 on the C3. 15 on tinypico
LED_COUNT = 50
ADC_PIN = 33  # 33 on Tinypico. 5 on Wemos s2 and c3.
DC_OFFSET = const(1255000)

pin = Pin(LED_PIN, Pin.OUT)
np = NeoPixel(pin, LED_COUNT)
adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)


# Try to get the max absolute value, over a 10ms period
async def getMaxRead() -> int:
    maxval = 0
    for i in range(0, 10):
        v = abs(adc.read_uv() - DC_OFFSET)
        if v > maxval:
            maxval = v
        # utime.sleep_us(1000)
        asyncio.sleep_ms(1)
    return maxval


# This is now working well with t(50, 1.5, 1, 100)
async def t(windowSize: int, q: float, delay: int, retriggerDelay: int):
    rollingAvg: float = 0
    lastTriggeredAt: int = 0
    maxInput: int = (
        2250000 / 2
    )  # 2250000 is claimed spec; dividing by two as don't seem to see it in practice
    ledValDivisor = maxInput / (LED_COUNT - 5)
    while True:
        v = await getMaxRead()
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

        if utime.ticks_diff(utime.ticks_ms(), lastTriggeredAt) < retriggerDelay:
            for i in range(LED_COUNT - 5, LED_COUNT):
                np[i] = (0, 64, 0)
        else:
            if rollingAvg > 90000 and v > q * rollingAvg:
                lastTriggeredAt = utime.ticks_ms()
                for i in range(LED_COUNT - 5, LED_COUNT):
                    np[i] = (0, 64, 0)

        np.write()
        # utime.sleep_ms(delay)
        asyncio.sleep_ms(delay)


try:
    asyncio.run(t(75, 1.4, 1, 100))
finally:
    asyncio.new_event_loop()
