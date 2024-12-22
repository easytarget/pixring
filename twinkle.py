from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms
from random import choice

# comment/uncomment and Modify the appropriate section below for your hardware,

# Expressif ESP32-C3 devboards have NeoPixes on GPIO8
#pixel = NeoPixel(Pin(8),1)
# SeeedStudio XIAO RP2040 (Pixel VCC is supplied via pin 11)
Pin(11, Pin.OUT).on()
pixel = NeoPixel(Pin(12), 1)

speedfactor = 50       # minimum flash interval in ms, make this lower to speed up
brightness  = 1.0      # A float between 0.0 and 1.0 that sets basic maximum brightness

# Use random indexes into tuples of possible values; this allows a 'bias' to be applied
# to favor faster and lower intensity flashes between bright long ones.
speeds = (1, 2, 3, 5)
values = (0, 1, 2, 3, 5, 7, 9, 11, 31, 63, 95, 127, 255)
colors = ((1,0,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1), (1,0,1), (1,1,1))

# Now twinkle, twinkle little star..
while True:
    value = int(choice(values) * brightness)
    color = choice(colors)
    pixel[0] = [c * value for c in color]
    pixel.write()
    sleep_ms(choice(speeds) * speedfactor)