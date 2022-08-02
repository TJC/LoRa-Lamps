import time
import network
import machine
import esp
import uasyncio as asyncio
from machine import SPI, Pin, I2C
from neopixel import NeoPixel
import ssd1306
import micropython

LED_PIN = 25  # as in built in led
led_pin = machine.Pin(25, machine.Pin.OUT)

# Screen - 128x64 via I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
disp = ssd1306.SSD1306_I2C(128, 64, i2c)
disp.text("Hello world!", 0, 0, 1)
disp.show()

#### ESP-NOW stuff

import network
import espnow

# import aioespnow
# the asyncio version has different methods
# https://micropython-glenn20.readthedocs.io/en/latest/library/espnow.html

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)  # .config(protocol=network.MODE_LR)
w0.active(True)
e = espnow.ESPNow()
e.active(True)

# broadcast mac address!
mac = b"\xff" * 6
e.add_peer(mac, channel=0, encrypt=False)
e.send(mac, "{message}", False)


## Reading be like
if e.any():
    [mac, msg] = e.recv(1)  # None is the timeout
    # Note: msg can be None
    print(msg)
