from machine import ADC, Pin
import array
import math
import utime
import uasyncio as asyncio
from espnowdriver import EspNowDriver

# For initial debugging only:
from neopixel import NeoPixel


# This class is designed to listen to an audio signal, and do beat detection.
# It assumes in the incoming audio signal has a 1.25V DC offset, and has already
# been passed through a low-pass filter.
# At time of writing, this is at ~240 Hz, by using a 20K resistor + 33 nF capacitor.
class AudioDriver:
    # The DC offset from the mic driver is 1.25V. The actual value read varies from device to device.
    DC_OFFSET = const(1255000)
    LED_COUNT = const(50)  # For initial debugging only

    # ADC only works on pins 1-10, and pins 1,3 are used internally.
    # Recommend pin 5 for now..
    def __init__(self, adcpin):
        self.adc = ADC(Pin(adcpin), atten=ADC.ATTN_11DB)
        # This attenuation reads up to 2450 mV; the default only goes to 1100mV. We need 2000mV.
        led_pin = 15  # 16 Lolin Wemos S2. Is pin 6 on the C3. 15 on tinypico
        self.leds = NeoPixel(Pin(led_pin, Pin.OUT), AudioDriver.LED_COUNT)

    # Try to get the max absolute value, over a 10ms period
    async def getMaxRead(self) -> int:
        maxval = 0
        for i in range(0, 10):
            v = abs(self.adc.read_uv() - AudioDriver.DC_OFFSET)
            if v > maxval:
                maxval = v
            # utime.sleep_us(1000)
            asyncio.sleep_ms(1)
        return maxval

    # This is now working well with t(1.7, 1, 100)
    async def audioBeatsDetection(self, q: float, delay: int, retriggerDelay: int):
        windowSize = const(75)
        rollingAvg: float = 0
        lastTriggeredAt: int = 0
        maxInput: int = (
            2250000 / 2
        )  # 2250000 is claimed spec; dividing by two as don't seem to see it in practice
        ledValDivisor = maxInput / (AudioDriver.LED_COUNT - 5)
        while True:
            v = await self.getMaxRead()
            rollingAvg -= rollingAvg / windowSize
            rollingAvg += v / windowSize
            self.leds.fill((0, 0, 0))

            # Show the average level
            ledCount = min(AudioDriver.LED_COUNT - 5, int(rollingAvg / ledValDivisor))
            for i in range(0, ledCount):
                self.leds[i] = (32, 0, 0)

            # Show the peak level
            peak = min(AudioDriver.LED_COUNT - 5, int(v / ledValDivisor))
            self.leds[peak] = (64, 64, 64)

            if utime.ticks_diff(utime.ticks_ms(), lastTriggeredAt) < retriggerDelay:
                for i in range(AudioDriver.LED_COUNT - 5, AudioDriver.LED_COUNT):
                    self.leds[i] = (0, 64, 0)
            else:
                if rollingAvg > 90000 and v > q * rollingAvg:
                    lastTriggeredAt = utime.ticks_ms()
                    # asyncio.create_task(EspNowDriver.send({"effect": "quickPulse"}))
                    await EspNowDriver.send({"effect": "quickPulse"})
                    for i in range(AudioDriver.LED_COUNT - 5, AudioDriver.LED_COUNT):
                        self.leds[i] = (0, 64, 0)

            self.leds.write()  # This takes 1.5ms for 50 LEDs.

            asyncio.sleep_ms(delay)
