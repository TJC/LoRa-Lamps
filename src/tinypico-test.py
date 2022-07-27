import time
import network
import machine
import esp
import uasyncio as asyncio
from machine import SPI, Pin
from neopixel import NeoPixel
import ssd1306
import tinypico
import micropython

LED_PIN = 27
LED_COUNT = 8

# Test code on the TinyPico


async def main():
    print(f"Current frequency: {machine.freq()}")
    # Show some info on boot
    print("Battery Voltage is {}V".format(TinyPICO.get_battery_voltage()))
    print("Battery Charge State is {}\n".format(TinyPICO.get_battery_charging()))

    # Show available memory
    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()

    t = asyncio.create_task(blink())
    await t


async def blink():
    # print("in blink")
    pin = machine.Pin(LED_PIN, machine.Pin.OUT)
    np = NeoPixel(pin, LED_COUNT)
    colours = [
        (128, 0, 0),
        (0, 128, 0),
        (0, 0, 128),
        (128, 128, 0),
        (128, 0, 128),
        (0, 128, 128),
        (128, 0, 0),
    ]
    idx = 0

    while True:
        # print("in blink loop..")
        np[0] = colours[idx]
        np[1] = colours[idx + 1]
        idx += 1
        if idx >= len(colours) - 1:
            idx = 0
        np.write()
        await asyncio.sleep_ms(500)


async def dispscreen():
    # sck = 18
    # mosi = 23
    # miso = 19 (unused)
    # dc = 21
    # cs = 22
    # rst = 33
    vspi = SPI(2, 100000)  # uses the 18/23/19 pins by default
    dc = Pin(21)  # data/command
    rst = Pin(33)  # reset
    cs = Pin(22)  # chip select
    disp = ssd1306.SSD1306_SPI(128, 160, vspi, dc, rst, cs)
    disp.text("Hello world!", 0, 0, 1)
    disp.show()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
