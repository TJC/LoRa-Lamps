import time
import network
import machine
import esp
import uasyncio as asyncio

# Test code for the generic ESP32 I had lying around


LED_PIN = 2

# LoRa
# IO23 = RESET
# IO18 = NSS/SEL
# IO5 = SCK
# IO27 = MOSI/SDI
# IO19 = MISO/SDO
# IO26 = DI0/IO0


async def main():
    # esp.osdebug(None)
    print(f"Current frequency: {machine.freq()}")
    # network.WLAN(network.STA_IF).active(False)
    t = asyncio.create_task(blink())
    await t


async def blink():
    # print("in blink")
    pin = machine.Pin(LED_PIN, machine.Pin.OUT)
    while True:
        # print("in blink loop..")
        pin.value(not pin.value())
        await asyncio.sleep_ms(500)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
