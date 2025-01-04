import math
from thisboard import ThisBoard


# Implements LED effects
# All functions must follow signature of:
# function(ledCount: int, elapsedMs: int) -> list[tuple[int,int,int]] | None
# use None to say that the effect has completed and should not be called any more.
class LightEffects:
    # Implements some simple lighting, used when no other effects are playing
    # For now, it's a solid warm-white breathing animation
    @staticmethod
    def idleLight(ledCount: int, elapsedMs: int):
        brightness = math.sin(math.pi * (elapsedMs % 10000) / 10000)
        r = 1 + int(30 * brightness)
        g = 1 + int(28 * brightness)
        b = 1 + int(25 * brightness)
        results = [(r, g, b)] * ledCount
        return results

    # A quick (200ms) pulse of green, might be used for bass beats?
    @staticmethod
    def quickPulse(ledCount: int, elapsedMs: int):
        brightness = 0.0
        if elapsedMs >= 200:
            return None
        elif elapsedMs >= 150:
            brightness = (200 - elapsedMs) / 50
        elif elapsedMs >= 50:
            brightness = 1.0
        else:
            brightness = 1.0 - (50 - elapsedMs) / 50

        g = int(255 * brightness)
        results = [(0, g, 0)] * ledCount
        return results

    # A medium speed (2000ms) red->blue transition with fade in/out
    @staticmethod
    def mediumRedBlue(ledCount: int, elapsedMs: int):
        brightness = 0.0
        if elapsedMs >= 2000:
            return None
        elif elapsedMs >= 1750:
            brightness = 1.0 - (250 - elapsedMs) / 250
        elif elapsedMs >= 250:
            brightness = 1.0
        else:
            brightness = (250 - elapsedMs) / 250

        r = 0.0
        b = 0.0
        if elapsedMs < 1000:
            r = min(1.0, (elapsedMs / 500))
            b = min(1.0, max(0, elapsedMs - 500) / 500)
        else:
            e = elapsedMs - 1000
            r = 1.0 - min(1.0, (e / 500))
            b = 1.0 - min(1.0, max(0, e - 500) / 500)

        r = int(255 * brightness * r)
        b = int(255 * brightness * b)
        results = [(r, 0, b)] * ledCount
        return results

    # Aims to take 450ms, and have a green light travel up the tower quickly, then
    # light the whole top part solidly
    @staticmethod
    def quickPulse2(ledCount: int, elapsedMs: int):
        results = [(0, 0, 0)] * ledCount
        if elapsedMs > 450:
            return None
        elif elapsedMs >= 400:
            for i in range(ThisBoard.initialTopLed, ThisBoard.finalTopLed + 1):
                results[i] = (0, 255, 0)
        elif elapsedMs >= 0:
            idx = int(
                ThisBoard.initialTowerLed
                + (
                    (ThisBoard.finalTowerLed - ThisBoard.initialTowerLed)
                    * (elapsedMs / 400)
                )
            )
            results[idx] = (0, 255, 0)
            if idx > 0:
                results[idx - 1] = (0, 255, 0)
            if idx < ThisBoard.finalTowerLed:
                results[idx + 1] = (0, 255, 0)
        else:
            return None

        return results
