import os
import utime
import machine
from machine import Pin

# Setup some common and useful functions depending on which board I'm using..
# For the moment, this just provides a common way to toggle the on-board LEDs,
# and blinks it three times at startup.
class CommonUtils:
    ledPin = None
    dotstar = None

    def init():
        if os.uname().machine.startswith("LOLIN_C3_MINI"):
            CommonUtils.ledPin = Pin(7, Pin.OUT)
        elif os.uname().machine.startswith("LILYGO TTGO LoRa32"):
            CommonUtils.ledPin = Pin(25, Pin.OUT)
        elif os.uname().machine.startswith("TinyPICO with ESP32-PICO-D4"):
            # TinyPico has fancy LED, but it requires a bunch more libraries to use it.
            # These consume around 10kbyte
            from machine import SoftSPI
            import tinypico as TinyPICO
            from dotstar import DotStar

            spi = SoftSPI(
                sck=Pin(TinyPICO.DOTSTAR_CLK),
                mosi=Pin(TinyPICO.DOTSTAR_DATA),
                miso=Pin(TinyPICO.SPI_MISO),
            )
            CommonUtils.dotstar = DotStar(
                spi, 1, brightness=0.5
            )  # Just one DotStar, half brightness
            TinyPICO.set_dotstar_power(True)

    def toggleLed():
        if CommonUtils.ledPin:
            CommonUtils.ledPin.value((CommonUtils.ledPin.value() + 1) % 2)
        elif CommonUtils.dotstar:
            if CommonUtils.dotstar[0][1] == 0:
                CommonUtils.dotstar[0] = (0, 127, 0)
            else:
                CommonUtils.dotstar[0] = (0, 0, 0)

    def tripleBlink():
        for i in range(0, 6):
            CommonUtils.toggleLed()
            utime.sleep(0.33)


CommonUtils.init()
CommonUtils.tripleBlink()
