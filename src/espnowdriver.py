import network
import uasyncio as asyncio
import aioespnow
import ujson
import os

# the asyncio version has different methods
# https://micropython-glenn20.readthedocs.io/en/latest/library/espnow.html


# Usage:
# EspNowDriver.init()
# asyncio.create_task(EspNowDriver.send({"foo": "bar"}))
# msg = await EspNowDriver.recv()
class EspNowDriver:
    myEspNow = None
    broadcastMac = b"\xff" * 6
    # The key is a very, very simple way to avoid unrelated JSON packets that might be getting
    # broadcast by other systems..
    key = 12345

    def init():
        # A WLAN interface must be active to send()/recv()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(protocol=network.MODE_LR)
        # This particular board requires setting this specific power to use wifi at all:
        if os.uname().machine.startswith("LOLIN_C3_MINI"):
            wlan.config(txpower=8.5)
        EspNowDriver.myEspNow = aioespnow.AIOESPNow()
        EspNowDriver.myEspNow.active(True)
        EspNowDriver.myEspNow.add_peer(
            EspNowDriver.broadcastMac, channel=0, encrypt=False
        )

    async def send(msg: object):
        msg["_key_"] = EspNowDriver.key
        j = ujson.dumps(msg)
        await EspNowDriver.myEspNow.asend(EspNowDriver.broadcastMac, j, False)

    async def heartbeat(period=2):
        i = 0
        while True:
            await EspNowDriver.send({"ping": i})
            i += 1
            await asyncio.sleep(period)

    # This is really just for testing at the moment
    async def recvLoop():
        while True:
            msg = await EspNowDriver.recv()
            print(f"ESPNOW:{msg}")
        # async for mac, msg in EspNowDriver.myEspNow:
        #     if msg != None:
        #         decoded = ujson.loads(msg)
        #         print("R:", decoded)

    async def recv():
        [mac, msg] = await EspNowDriver.myEspNow.arecv()
        print("Raw:", msg)
        if msg != None:
            try:
                decoded = ujson.loads(msg)
                if decoded["_key_"] != EspNowDriver.key:
                    decoded = None
            except (KeyError, ValueError):
                decoded = None
            return decoded
        return None


# For copy-paste testing:
# EspNowDriver.init()
# asyncio.new_event_loop()
# asyncio.run(EspNowDriver.recvLoop())
# asyncio.run(EspNowDriver.heartbeat())
