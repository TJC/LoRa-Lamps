import os
import utime
import machine
from machine import Pin


# Functions to detect which board we're running on right now, and return info
# about which pins are connected to which peripherals.
# Right now they all hardcode the same number of external LEDs, but I think I'll want to set
# that more dynamically later.
# One thought is to flash a dedicated metadata class file to each board, separately to the rest?
class Boards:
    lolin_c3 = {
        "name": "Lolin C3",
        "internalLedPin": 7,
        "extLedPin": 6,
        "ledCount": 87,
        "gpsRxPin": 25,
        "gpsTxPin": 26,
        "pirPin": 7,
        "adcPin": None,
        "mode": "dev",
    }

    lolin_s2 = {
        "name": "Lolin S2",
        "internalLedPin": 15,
        "extLedPin": 16,  # same physical pin as C3
        "ledCount": 87,
        "gpsRxPin": 37,
        "gpsTxPin": 39,
        "pirPin": 11,
        "adcPin": 5,
        "mode": "dev",
    }

    tinypico = {
        "name": "TinyPICO",
        "internalLedPin": None,  # It does, but it's a Dotstar over SPI
        "extLedPin": 15,
        "ledCount": 87,
        "gpsRxPin": None,
        "gpsTxPin": None,
        "pirPin": None,
        "adcPin": 33,
        "mode": "dev",
    }

    lilygo_lora32 = {
        "name": "Lilygo LoRa32",
        "internalLedPin": 25,
        "extLedPin": 15,
        "ledCount": 87,
        "gpsRxPin": None,
        "gpsTxPin": None,
        "pirPin": None,
        "adcPin": None,
        "mode": "dev",
    }

    # I think I'll want to implement both basic machine-level info, and then overrides based on something else..
    # (ie. for different modes or numbers of LEDs..)
    def metadata():
        if os.uname().machine.startswith("LOLIN_C3_MINI"):
            return Boards.lolin_c3
        elif os.uname().machine.startswith("LILYGO TTGO LoRa32"):
            return Boards.lilygo_lora32
        elif os.uname().machine.startswith("TinyPICO with ESP32-PICO-D4"):
            return Boards.tinypico
        elif os.uname().machine.startswith("LOLIN_S2_MINI"):
            return Boards.lolin_s2
        else:
            raise RuntimeError("Unknown board: " + os.uname().machine)
