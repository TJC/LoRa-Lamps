import uasyncio as asyncio
from neopixeldriver import NeopixelDriver
from motionsensor import MotionSensor
from espnowdriver import EspNowDriver
from gpsdriver import GpsDriver
from initial_self_test import InitialSelfTest
from boards import Boards
import micropython


async def main():
    print("Starting up")
    board = Boards.metadata()
    InitialSelfTest().run()

    EspNowDriver.init()
    # ESP-NOW will be replaced by LoRa eventually

    if board["extLedPin"] != None:
        NeopixelDriver.init()
        await NeopixelDriver.addEffect("idleLight")
        asyncio.create_task(NeopixelDriver.mainLoop())

    # if board["gpsRxPin"] != None:
    #     GpsDriver()

    # if board["pirPin"] != None:
    #     MotionSensor.init()
    #     asyncio.create_task(MotionSensor.watchSensor())

    # Simulate some events until we get real ones:
    await NeopixelDriver.addEffect("mediumRedBlue")
    await simulate130bpm()

    # TODO: Listen for ESP-NOW events, and trigger effects from them.


# Until we get some proper audio support:
async def simulate130bpm():
    while True:
        await asyncio.sleep_ms(461)  # 130 bpm
        await NeopixelDriver.addEffect("quickPulse")


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
