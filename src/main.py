import uasyncio as asyncio
from neopixeldriver import NeopixelDriver
from motionsensor import MotionSensor
from espnowdriver import EspNowDriver
from gpsdriver import GpsDriver
from audiodriver import AudioDriver
from initial_self_test import InitialSelfTest
from boards import Boards
import micropython
import ujson


async def testMain():
    print("Starting up testMain()")
    board = Boards.metadata()
    InitialSelfTest().run()

    NeopixelDriver.init()
    # await NeopixelDriver.addEffect("idleLight")
    asyncio.create_task(NeopixelDriver.mainLoop())

    # Simulate some events until we get real ones:
    await simulate130bpm()


async def eventReceiverMain():
    print("Starting up")
    board = Boards.metadata()
    InitialSelfTest().run()

    EspNowDriver.init()
    # ESP-NOW will be replaced by LoRa eventually

    if board["extLedPin"] != None:
        NeopixelDriver.init()
        # await NeopixelDriver.addEffect("idleLight")
        asyncio.create_task(NeopixelDriver.mainLoop())

    # if board["gpsRxPin"] != None:
    #     GpsDriver()

    # if board["pirPin"] != None:
    #     MotionSensor.init()
    #     asyncio.create_task(MotionSensor.watchSensor())

    # Simulate some events until we get real ones:
    # await simulateSlowPulse()
    # await simulate130bpm()

    # TODO: Listen for ESP-NOW events, and trigger effects from them.
    async for mac, msg in EspNowDriver.myEspNow:
        if msg != None:
            await handleIncomingEvent(msg)


async def handleIncomingEvent(msg):
    try:
        decoded = ujson.loads(msg)
        print("ESPNOW: ", decoded)
        if decoded["effect"] == "quickPulse":
            await NeopixelDriver.addEffect("quickPulse")
    except:
        print("Error decoding message")


async def audioInputMain():
    print("Starting up")
    board = Boards.metadata()
    InitialSelfTest().run()

    EspNowDriver.init()
    # ESP-NOW will be replaced by LoRa eventually

    await EspNowDriver.send({"notice": "Audio driver starting up"})

    audioDriver = AudioDriver(board["adcPin"])
    await audioDriver.audioBeatsDetection(1.7, 1, 250)


# Until we get some proper audio support:
async def simulate130bpm():
    while True:
        await asyncio.sleep_ms(461)  # 130 bpm
        await NeopixelDriver.addEffect("quickPulse2")


async def simulateSlowPulse():
    while True:
        await asyncio.sleep_ms(5000)  # 130 bpm
        await NeopixelDriver.addEffect("mediumRedBlue")


# import main
# import uasyncio as asyncio
# try:
#     asyncio.run(main.audioInputMain())
#     asyncio.run(main.eventReceiverMain())
#     asyncio.run(main.testMain())
# finally:
#     asyncio.new_event_loop()
