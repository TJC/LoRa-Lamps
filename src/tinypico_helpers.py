class TinyPicoHelpers:
    dotstar = None

    def init():
        from machine import Pin
        from machine import SoftSPI
        import tinypico as TinyPICO
        from dotstar import DotStar

        spi = SoftSPI(
            sck=Pin(TinyPICO.DOTSTAR_CLK),
            mosi=Pin(TinyPICO.DOTSTAR_DATA),
            miso=Pin(TinyPICO.SPI_MISO),
        )
        TinyPicoHelpers.dotstar = DotStar(
            spi, 1, brightness=0.5
        )  # Just one DotStar, half brightness
        TinyPICO.set_dotstar_power(True)
