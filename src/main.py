import uasyncio as asyncio
from neopixeldriver import NeopixelDriver
from motionsensor import MotionSensor
from espnowdriver import EspNowDriver
from initial_self_test import InitialSelfTest
from boards import Boards


async def main():
    print("Starting up")
    board = Boards.metadata()
    InitialSelfTest().run()

    if board["extLedPin"] != None:
        NeopixelDriver.init()

    # if board["pirPin"] != None:
    #     MotionSensor.init()
    #     asyncio.create_task(MotionSensor.watchSensor())

    # asyncio.create_task(NeopixelDriver.fire2022())

    # await NeopixelDriver.mainLoop()


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
