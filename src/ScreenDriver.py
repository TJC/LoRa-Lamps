import uasyncio as asyncio
from machine import Pin, I2C
import ssd1306

# Driver for the OLED screen on the LoRa32
# maybe 128x64?
# I think connected on I2C.
# SDA 21
# SCL 22
# There is no Reset pin.


class ScreenDriver:
    def __init__(self):
        i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
        self.display = ssd1306.SSD1306_I2C(128, 64, i2c)

    def print(self, msg):
        # TODO: wrap text over more lines if it's longer than 16 chars,
        # or if it contains newlines.
        self.display.text(msg, 0, 0, 1)
        self.display.show()
