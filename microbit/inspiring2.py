from microbit import *

# I found this approach on the web, apologies to the creator I cant get back to the blog to provide the link.
# I will update when I can.
# The only thing I had to change was the final write to indicate update. The blog used 0xff, this did not work
# When I change to 0x0 as per the original inspiring code it did.
# Using an external 2 amp PSU to power the leds, I have managed to control all 136 of my leds.
# Well 135, one of them has failed on the circular ring

spi.init()

num_leds = 136
on_pixel = 5

x = 0xff  # full brightness
r = 0x0f  # full red
g = 0x00
b = 0x00
buf = bytearray([x, b, g, r])

# start frame
def leds_off():
    spi.write(b'\x00\x00\x00\x00')
    for i in range(num_leds):
        spi.write(b'\xff\x00\x00\x00')  # all off
    spi.write(b'\x00\x00\x00\x00')  #spi.write(b'\xff\xff\xff\xff')
    

def one_led(buf):
    # light up leds
    while True:
        sleep(1)
        spi.write(b'\x00\x00\x00\x00')
        for i in range(num_leds):
            if i == on_pixel:
                spi.write(buf)
            else:
                spi.write(b'\xff\x0f\x00\x00')
        spi.write(b'\x00\x00\x00\x00')  #spi.write(b'\xff\xff\xff\xff')

def bounce(buf):

    while True:
        for j in range(num_leds):
            sleep(15)
            spi.write(b'\x00\x00\x00\x00')
            for i in range(num_leds):
                if i == j:
                    spi.write(buf)
                else:
                    spi.write(b'\xff\x00\x00\x00')
            spi.write(b'\x00\x00\x00\x00')

        for k in range(num_leds-1, -1, -1):
            sleep(15)
            spi.write(b'\x00\x00\x00\x00')
            for i in range(num_leds):
                if i == k:
                    spi.write(buf)
                else:
                    spi.write(b'\xff\x00\x00\x00')
            spi.write(b'\x00\x00\x00\x00')
        sleep(1000)

def grow(buf):
    while True:
        for j in range(num_leds):
            spi.write(b'\x00\x00\x00\x00')
            for i in range(j):
                spi.write(buf)
            spi.write(b'\x00\x00\x00\x00')
            sleep(100)
        for j in range(num_leds-1, -1, -1):
            spi.write(b'\x00\x00\x00\x00')
            for i in range(j):
                spi.write(buf)
            for k in range(j, num_leds, 1) :
                spi.write(b'\xff\x00\x00\x00')
            spi.write(b'\x00\x00\x00\x00')
            
            sleep(100)


display.show(Image.SAD)
leds_off()
sleep(10)
display.show(Image.HAPPY)
#one_led()
#bounce(buf)
grow(buf)
