from machine import ADC, Pin
import utime

ADC_PIN = 33  # 33 on Tinypico. 5 on Wemos s2.
DC_OFFSET = const(20987)
# dc offset seems more like 20987 on Tinypico?
# But 31300 on Wemos S2??? And different on C3 as well!


# Doing some tests with a 1.336V source voltage:
# Wemos S2: 33441 (avg)
# Tinypico: 24266 (avg)
# Wemos C3: 28969 (avg)

# Looks like using read_uv() returns much more consistent results.
# Shall swap to that..


def adcreader():
    adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)
    while True:
        v = adc.read_u16()
        print(v)
        utime.sleep_ms(250)


def adcreader2():
    adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)
    while True:
        v = adc.read_uv()
        print(v)
        utime.sleep_ms(250)


def adcinfo():
    adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)
    mymin = 9000000
    mymax = 0
    mysum = 0
    mycount = 0
    startms = utime.ticks_ms()
    for i in range(0, 20000):
        v = adc.read_uv()
        mysum += v
        mycount += 1
        if v > mymax:
            mymax = v
        if v < mymin:
            mymin = v
    endms = utime.ticks_ms()
    print(f"Elapsed ms: {endms - startms}")
    print(f"Min: {mymin}")
    print(f"Max: {mymax}")
    myavg = int(mysum / mycount)
    print(f"Avg: {myavg}")
