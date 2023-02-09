import utime
from machine import Pin

pin = Pin(7, Pin.IN)

# As the built-in LED is already on pin 7 (oops), this means the PIR will trigger the LED for us!
