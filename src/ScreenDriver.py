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

    # TODO: Wrap lines that are 16+ characters long?
    def print(self, msg):
        yOffset = 0
        self.display.fill(0)
        lines = msg.split()
        for line in lines:
            self.display.text(line, 0, yOffset, 1)
            yOffset += 9
        self.display.show()
