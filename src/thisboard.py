# This class contains individual board-specific specs and modes
# ie. Because each "lamp" can have different sensors or numbers of LEDs.


#            Tower        Top
# Lamp A:   0 - 52      63 - 81
# Lamp B:   0 - 54      66 - 85
# Lamp C:   0 - 48      58 - 77
class ThisBoard:
    # The *Led items are indexes into the LED array
    initialTowerLed = const(0)
    finalTowerLed = const(54)
    ledCountTower = const(55)

    initialTopLed = const(63)
    finalTopLed = const(85)
    ledCountTop = const(23)
