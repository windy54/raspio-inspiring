from microbit import *
import array
# the API is likely to change, and may change in ways that break existing code.

# this is a port of apa.py to the microbit.
# I have modified how the leds are stored to use bytearray, thanks to some help
# from the micropyton forum.

DELAY = 20


class Apa:
    def __init__(self, num_leds):
        self.leds = bytearray(4 + num_leds * 4 + 4)


    def show(self):
        spi.write(self.leds)
       

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
        self.leds[4 + 4 * n + 0] = self.limit(intensity)
        self.leds[4 + 4 * n + 1] = r
        self.leds[4 + 4 * n + 2] = b
        self.leds[4 + 4 * n + 3] = g


def blue_demo(num_leds):
    # bar has 8 leds
    apa = Apa(num_leds)

    # initialise the SPI bus using defaults.
    # Pin 13 of the microbit is therefore used as CI (SCLCK) - the clock
    # Pin 15 of the microbit is used as DI (MOSI) - the data

   

    # turn each LED blue

    for i in range(num_leds):
        apa.set_led (i, 0x30, 0x0, 0x0, 10)
        apa.show()
        sleep(100)
    # turn each LED off

    for i in range(num_leds):
        apa.set_led(i, 0x0, 0x0, 0x0, 0x0)
        apa.show()
        sleep(100)


def multi_colours(num_leds):

    apa = Apa(num_leds)
    
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
    apa = Apa(num_leds)
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
    spi.init()
    # blue_demo()
    display.show(Image.HAPPY)
    # multi_colours(64)
    fast_leds(136)
