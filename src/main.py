import uasyncio as asyncio
from neopixeldriver import NeopixelDriver
from motionsensor import MotionSensor
from espnowdriver import EspNowDriver


async def main():
    print("Starting up")
    NeopixelDriver.init()
    MotionSensor.init()
    asyncio.create_task(NeopixelDriver.fire2022())
    asyncio.create_task(MotionSensor.watchSensor())
    await NeopixelDriver.mainLoop()


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
