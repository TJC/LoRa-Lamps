from machine import Pin, ADC

# ADC supports 8 to 12 bit reads
# 10 bit is used here, meaning values of 0-1023

class SmoothedADC():
    SAMPLE_COUNT = 20

    def __init__(self, io_pin):
        self.adc = self.setup_adc(io_pin)
        self.recent_values = [512] * self.SAMPLE_COUNT

    def setup_adc(self, pin):
        i = ADC(Pin(pin))
        i.atten(ADC.ATTN_11DB)       #Full range: 3.3v
        i.width(ADC.WIDTH_10BIT)
        return i

    # Return 0-1023 value .. not sure if I'll actually use this.
    def read8bit(self):
        self.recent_values.pop(0)
        self.recent_values.append(self.adc.read())
        return round(sum(self.recent_values) / self.SAMPLE_COUNT)

    # Return 0.0 to 1.0 value:
    def read(self):
        self.recent_values.pop(0)
        self.recent_values.append(self.adc.read())
        return sum(self.recent_values) / self.SAMPLE_COUNT / 1023.0
