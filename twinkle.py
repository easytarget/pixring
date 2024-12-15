from machine import Pin
import neopixel
from utime import sleep
from random import choice

pixel = neopixel.NeoPixel(Pin(12), 1)
pixelPower = Pin(11, Pin.OUT)
pixelPower.on()

speeds = range(1,6,1)
speedfactor = 0.1
intensities = [1,2,3,7,15,31,47,63,95,127,255]

while True:
    val = choice(intensities)
    cycle = [(val,0,0),(val,val,0),(0,val,0),(0,val,val),(0,0,val),(val,0,val),(val,val,val)]
    #cycle = [(val,val,val),(val,val,0),(val,val,val),(0,val,val),(val,val,val),(val,0,val)]
    for pixel[0] in cycle:
        pixel.write()
        sleep(choice(speeds)*speedfactor)