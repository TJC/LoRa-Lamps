import uasyncio as asyncio
from machine import Pin
from neopixel import NeoPixel
from adafruit_fancyled import adafruit_fancyled as fancyled
import utime
from boards import Boards
from lighteffects import LightEffects


class NeopixelDriver:
    LED_COUNT = 1  # Updated by init()
    leds: NeoPixel = None
    effectLeds: list[tuple[int, int, int]] = [(0, 0, 0)] * LED_COUNT

    trigger: asyncio.Event = None
    # You then use:
    # await NeopixelDriver.trigger.wait()
    # NeopixelDriver.trigger.clear()
    # (in other thread) NeopixelDriver.trigger.set()

    # Contains tuples of effect id, and start time
    # TODO: Function pointers instead of ids?
    effectList: list[tuple[str, int]] = []

    effectListLock = asyncio.Lock()

    def init():
        boardInfo = Boards.metadata()
        pin = Pin(boardInfo["extLedPin"], Pin.OUT)
        NeopixelDriver.LED_COUNT = boardInfo["ledCount"]
        NeopixelDriver.leds = NeoPixel(pin, NeopixelDriver.LED_COUNT)
        NeopixelDriver.trigger = asyncio.Event()

    async def addEffect(id: str):
        async with NeopixelDriver.effectListLock:
            i = (id, utime.ticks_ms())
            NeopixelDriver.effectList.append(i)

    # Remove an item from the list, by INDEX not id.. (since we might have multiple effects at the same time)
    async def removeEffectId(idx: int):
        async with NeopixelDriver.effectListLock:
            del NeopixelDriver.effectList[idx]

    async def mainLoop():
        while True:
            effects = []
            currentTicks = utime.ticks_ms()
            NeopixelDriver.leds.fill((0, 0, 0))

            # Take a local copy of the effects list safely
            async with NeopixelDriver.effectListLock:
                effects = NeopixelDriver.effectList

            for idx, item in enumerate(effects):
                (id, startMs) = item
                # print(f"Proc effect {id}")

                results = NeopixelDriver.procEffect(
                    id, NeopixelDriver.LED_COUNT, currentTicks - startMs
                )
                if results == None:
                    # XXX bug here, index won't be consistent or constant
                    await NeopixelDriver.removeEffectId(idx)
                else:
                    # Integrate effects
                    for i in range(0, NeopixelDriver.LED_COUNT):
                        NeopixelDriver.leds[i] = NeopixelDriver.mergeWithClamp(
                            NeopixelDriver.leds[i], results[i]
                        )

            # print("Writing LEDs. First LED = " + str(NeopixelDriver.leds[0]))
            NeopixelDriver.leds.write()
            await asyncio.sleep_ms(20)

    # Just a factory method until we use function pointers instead of ids..
    def procEffect(id: str, ledCount: int, elapsedMs: int):
        if id == "idleLight":
            return LightEffects.idleLight(ledCount, elapsedMs)
        elif id == "quickPulse":
            return LightEffects.quickPulse(ledCount, elapsedMs)
        elif id == "mediumRedBlue":
            return LightEffects.mediumRedBlue(ledCount, elapsedMs)
        else:
            print(f"Unknown effect id: {id}")
            return None

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


# from neopixeldriver import NeopixelDriver
# NeopixelDriver.init()
# import uasyncio
# uasyncio.run(NeopixelDriver.fire2022())
