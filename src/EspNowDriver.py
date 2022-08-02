import network
import uasyncio as asyncio
import aioespnow

# the asyncio version has different methods
# https://micropython-glenn20.readthedocs.io/en/latest/library/espnow.html


class EspNowDriver:
    wlan = None
    myEspNow = None

    def __init__(self):
        # A WLAN interface must be active to send()/recv()
        EspNowDriver.wlan = network.WLAN(network.STA_IF)
        # .config(protocol=network.MODE_LR)
        EspNowDriver.wlan.active(True)
        EspNowDriver.espnow = aioespnow.AIOESPNow()
        EspNowDriver.myEspNow.active(True)
        broadcastMac = b"\xff" * 6
        EspNowDriver.myEspNow.add_peer(broadcastMac, channel=0, encrypt=False)

    async def send(msg):
        await EspNowDriver.myEspNow.asend(msg)

    async def heartbeat(period=30):
        i = 0
        while True:
            await EspNowDriver.myEspNow.asend(f"ping {i}")
            i += 1
            await asyncio.sleep(period)

    async def recvLoop():
        async for mac, msg in EspNowDriver.myEspNow:
            print("R:", msg)

    async def recv():
        [mac, msg] = await EspNowDriver.myEspNow.arecv()
        print("R:", msg)
