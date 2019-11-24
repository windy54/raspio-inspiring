from microbit import *
import array
# the API is likely to change, and may change in ways that break existing code.

# this is a port of apa.py to the microbit.
# It works for 64 leds, when 65 leds are selected the program crashes
# I have done some investigation and it seems that each time a new element in self.leds is created
# 32 36 bytes of data are used. Eventually at 65 elements the microbit runs out of memory
# I have investigated on a PI and there 32 bytes are used to create the self.leds object and an additional 4 bytes
# are used per element.

DELAY = 200


class Apa:
    def __init__(self, num_leds):
        self.buffer = bytearray(4)
        self.leds = [array.array('b',[0xE0, 0, 0x0, 0]) for i in range(num_leds)]


    def show(self):
        spi.write(b'\x00\x00\x00\x00')
        for led in self.leds:
            for i in range(4):
                self.buffer[i] = led[i]
            spi.write(self.buffer)
        spi.write(b'\x00\x00\x00\x00')

    def limit(self, intensity):
        # intensity ranges from 0 (off) to 31 (very bright)
        # but leading three bits must be set to 1, so add 0xE0
        offset = 0xE0
        if intensity < 0:
            return offset
        if intensity > 31:
            return offset + 31
        return offset + intensity

    # allow indexing
    def __getitem__(self, item):
        return self.leds[item]

    # allow indexed assignment
    def __setitem__(self, key, value):
        self.set_led(key, *value)

    # low-level set method allows default intensity, adjusts intensity value
    def set_led(self, n, r, b, g, intensity=5):
        self.leds[n][0] = self.limit(intensity)
        self.leds[n][1] = r
        self.leds[n][2] = b
        self.leds[n][3] = g


def blue_demo(num_leds):
    # bar has 8 leds
    apa = Apa(num_leds)

    # initialise the SPI bus using defaults.
    # Pin 13 of the microbit is therefore used as CI (SCLCK) - the clock
    # Pin 15 of the microbit is used as DI (MOSI) - the data

    spi.init()

    # turn each LED blue

    for i in range(num_leds):
        apa[i] = (0x30, 0x0, 0x0, 10)
        apa.show()
        sleep(100)
    # turn each LED off

    for i in range(num_leds):
        apa[i] = (0x0, 0x0, 0x0, 0x0)
        apa.show()
        sleep(100)


def multi_colours(num_leds):

    apa = Apa(num_leds)
    spi.init()
    # repeat until button A is pressed
    while button_a.get_presses() == 0:
        for i in range(num_leds):
            apa.set_led(i, 0xFF, 0, 0)
            apa.show()
            sleep(DELAY)
            apa.set_led(i, 0, 0xFF, 0)
            apa.show()
            sleep(DELAY)
            apa.set_led(i, 0, 0, 0xFF)
            apa.show()
            sleep(DELAY)
            apa.set_led(i, 0, 0, 0, 0)
            apa.show()
            sleep(DELAY)


def fast_leds(num_leds):
    display.show("F")
    apa = Apa(num_leds)
    display.show("A")
    sleep(200)
    spi.init()
    display.show("I")
    # repeat until button A is pressed
    while button_a.get_presses() == 0:
        for i in range(num_leds):
            apa.set_led(i, 0xFF, 0, 0)
            apa.show()
            sleep(DELAY)
            apa.set_led(i, 0, 0, 0, 0)
            apa.show()
            sleep(DELAY)


if __name__ == '__main__':
    # blue_demo()
    display.show(Image.HAPPY)
    # multi_colours(64)
    fast_leds(64)
