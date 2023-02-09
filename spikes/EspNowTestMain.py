from screendriver import ScreenDriver
from espnowdriver import EspNowDriver
import uasyncio as asyncio

screen = ScreenDriver()
screen.print("Init!")

EspNowDriver.init()


async def mainLoop():
    while True:
        msg = await EspNowDriver.recv()
        print(msg)
        screen.print(f"ping: {msg['ping']}\nsrc: {msg['sender']}")


asyncio.run(mainLoop())
