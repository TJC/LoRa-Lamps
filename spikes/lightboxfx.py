from machine import ADC, Pin
from neopixel import NeoPixel
import utime

LED_PIN = 6  # 16 Lolin Wemos S2. Is pin 6 on the C3. 15 on tinypico
LED_COUNT = 6
ADC_PIN = 2  # 33 on Tinypico. 5 on Wemos s2 and c3. 2 on the C3 I messed up..
DC_OFFSET = const(1255000)


class BoxTrigger:
    decayPeriod = const(1000)  # millis

    def __init__(self, boxId, colour, v) -> None:
        self.boxId = boxId
        self.colour = colour
        self.v = v
        self.startTime = utime.ticks_ms()

    def v(self) -> int:
        return self.v

    def decay(self, nowTime) -> None:
        elapsed = max(1, min(BoxTrigger.decayPeriod, (nowTime - self.startTime)))
        amount = 1.0 - elapsed / BoxTrigger.decayPeriod

        self.v = amount * self.v
        if self.v <= 1:
            self.v = 0

    def isNotFinished(self) -> bool:
        return self.v >= 2

    def rgb(self):
        v = int(self.v)
        if self.colour == 0:
            return (v, 0, 0)
        elif self.colour == 1:
            return (0, v, 0)
        elif self.colour == 2:
            return (0, 0, v)


class LightboxFX:
    def __init__(self) -> None:
        pin = Pin(LED_PIN, Pin.OUT)
        self.np = NeoPixel(pin, LED_COUNT)
        self.adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)
        self.triggers: list[BoxTrigger] = []
        self.lastBox = 0
        self.numBoxes = 3
        self.lastColour = 0
        self.numColours = 3

    # Try to get the max absolute value, over a 10ms period
    def getMaxRead(self) -> int:
        maxval = 0
        for i in range(0, 10):
            v = abs(self.adc.read_uv() - DC_OFFSET)
            if v > maxval:
                maxval = v
            utime.sleep_us(1000)
        return maxval

    def mainloop(self, q: float, retriggerDelay: int) -> None:
        windowSize = const(75)
        rollingAvg: float = 0
        lastTriggeredAt: int = 0

        while True:
            v = self.getMaxRead()
            rollingAvg -= rollingAvg / windowSize
            rollingAvg += v / windowSize

            self.updateTriggerValues()

            if utime.ticks_diff(utime.ticks_ms(), lastTriggeredAt) >= retriggerDelay:
                if rollingAvg > 90000 and v > q * rollingAvg:
                    lastTriggeredAt = utime.ticks_ms()
                    self.addTrigger()

            self.writeBoxes()
            self.sweepFinishedTriggers()
            utime.sleep_ms(1)

    # Note that my current demo has two LEDs per box, but that will probably change in final version
    # Thus the t*2 stuff might need to change.
    def writeBoxes(self) -> None:
        self.np.fill((0, 0, 0))

        for t in self.triggers:
            curPixVal = self.np[t.boxId * 2]
            thisVal = t.rgb()
            newVal = self.mergeRGB(curPixVal, thisVal)
            self.np[t.boxId * 2] = self.np[(t.boxId * 2) + 1] = newVal

        self.np.write()

    def mergeRGB(self, a, b):
        r = min(255, a[0] + b[0])
        g = min(255, a[1] + b[1])
        b = min(255, a[2] + b[2])
        return (r, g, b)

    def addTrigger(self) -> None:
        box = (self.lastBox + 1) % self.numBoxes
        colour = (self.lastColour + 1) % self.numColours
        self.triggers.append(BoxTrigger(box, colour, 255))
        self.lastBox = box
        self.lastColour = colour

    def sweepFinishedTriggers(self) -> None:
        newList: list[BoxTrigger] = filter(lambda i: (i.isNotFinished()), self.triggers)
        self.triggers = list(newList)

    def updateTriggerValues(self) -> None:
        nowTime = utime.ticks_ms()
        for t in self.triggers:
            t.decay(nowTime)


# from lightboxfx import LightboxFX
# LightboxFX().mainloop(1.7, 250)
# LightboxFX().mainloop(1.5, 200)
