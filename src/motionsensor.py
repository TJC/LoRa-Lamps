import utime
from machine import Pin
import uasyncio as asyncio
from neopixeldriver import NeopixelDriver
from boards import Boards


class MotionSensor:
    flag = None
    pin = None
    # As the built-in LED is already on pin 7 (oops), this means the PIR will trigger the LED for us!
    # Oh well, at least we don't need a pull-down resistor..
    hasLeds = False

    def init():
        board = Boards.metadata()
        pinId = board["pirPin"]
        if board["extLedPin"]:
            MotionSensor.hasLeds = True
        MotionSensor.pin = Pin(pinId, Pin.IN)
        MotionSensor.flag = asyncio.ThreadSafeFlag()
        MotionSensor.pin.irq(trigger=Pin.IRQ_RISING, handler=MotionSensor.irqHandler)

    def irqHandler(pin: Pin):
        MotionSensor.flag.set()

    async def watchSensor():
        while True:
            await MotionSensor.flag.wait()
            print("Motion sensed!")
            # TODO: Emit an ESP-NOW event
            if MotionSensor.hasLeds:
                await NeopixelDriver.addEffect("mediumRedBlue")


# import uasyncio
# uasyncio.run(MotionSensor.watchSensor())
