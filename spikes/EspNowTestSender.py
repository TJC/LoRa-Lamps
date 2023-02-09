from espnowdriver import EspNowDriver
import uasyncio as asyncio

EspNowDriver.init()


async def mainLoop(sender):
    i = 0
    while True:
        await EspNowDriver.send({"ping": i, "sender": sender})
        i += 1
        await asyncio.sleep(3)


asyncio.run(mainLoop("wemos c3"))
