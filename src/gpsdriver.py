import machine
import uasyncio as asyncio
from as_GPS import DD, AS_GPS
from boards import Boards


class GpsDriver:
    def __init__(self) -> None:
        print("Initialising GPS")
        board = Boards.metadata()
        uart = machine.UART(
            1,
            rx=board["gpsRxPin"],
            tx=board["gpsTxPin"],
            baudrate=9600,
            bits=8,
            parity=None,
            stop=1,
            timeout=5000,
            rxbuf=1024,
        )

        sreader = asyncio.StreamReader(uart)
        self.gps = AS_GPS(sreader)

    # Attempts to return current location as a (lat,long) tuple, converting the S and W versions to negative numbers
    def current_location(self) -> tuple[float, float]:
        (lat, latDir) = self.gps.latitude(DD)
        if latDir == "S":
            lat = -lat

        (long, longDir) = self.gps.longitude(DD)
        if longDir == "W":
            long = -long

        return [lat, long]

    # Print stats every 10 seconds. useful when debugging
    async def stats(self):
        while True:
            await asyncio.sleep(10)
            print("***** STATISTICS *****")
            print("Sentences Found:", self.gps.clean_sentences)
            print("Sentences Parsed:", self.gps.parsed_sentences)
            print("Satellites in view:", self.gps.satellites_in_view)
            print("Satellites in use:", self.gps.satellites_in_use)
            print("CRC_Fails:", self.gps.crc_fails)
            print()

    # Print navigation data every 4s. useful when debugging
    async def navigation(self):
        while True:
            await asyncio.sleep(2)
            await self.gps.data_received(position=True)
            print("***** NAVIGATION DATA *****")
            print("Data is Valid:", self.gps._valid)
            print("Lat, Long:", self.current_location())
            print("Accuracy (HDOP):", self.gps.hdop)
            print()

    async def gps_test(self):
        print("awaiting first fix")
        asyncio.create_task(self.stats())
        asyncio.create_task(self.navigation())

        # This just exists while debugging on the REPL:
        while True:
            await asyncio.sleep_ms(1000)


# from gpsdriver import GpsDriver
# asyncio.new_event_loop()
# asyncio.run(GpsDriver().gps_test())
