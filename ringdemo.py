from pixrings import PixRing
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms
from random import randint

'''
    demo

    Important:
    Adjust the Pin Information below to match your wiring

'''

#pix_pin = Pin(26)
pix_pin = Pin(3)
num_pix = 124
np = NeoPixel(pix_pin, num_pix)


ringlist = [45,35,24,12,8]
ringtotal = len(ringlist)
ringz = PixRing(np,ringlist)

# limits and spread
minb = 1
maxb = 12
sfac = 1  # spread factor

ringz.set()
cont = True

while cont:
    # fadeup
    for ring in range(ringtotal - 1, -1, -1):
        r = g = b = 0
        rmax = randint(1,maxb)
        gmax = randint(1,maxb)
        bmax = randint(1,maxb)
        for step in range(max(rmax, gmax, bmax)):
            r = min(rmax, r + 1)
            g = min(gmax, g + 1)
            b = min(bmax, b + 1)
            ringz.set(ring,(r, g, b))
            sleep_ms(int(50 / sfac))

    sleep_ms(100)

    # Random ring colors
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ringz.set(randint(0,ringtotal - 1),(randint(minb,maxb),randint(minb,maxb),randint(minb,maxb)))
        sleep_ms(randint(0,100))

    # random color movements
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ring = randint(0,ringtotal - 1)
        r = max(minb,min(maxb, ringz.rings[ring][0][1][0] + randint(-sfac,sfac)))
        g = max(minb,min(maxb, ringz.rings[ring][0][1][1] + randint(-sfac,sfac)))
        b = max(minb,min(maxb, ringz.rings[ring][0][1][2] + randint(-sfac,sfac)))
        ringz.set(ring,(r,g,b))

    # Cler
    ringz.set()

    # Random spokes
    end = ticks_ms() + 1500
    while ticks_ms() < end:
        angle  = randint(0,359)
        ringz.pos(rgb=(randint(minb,maxb),randint(minb,maxb),randint(minb,maxb)),pos=angle,units='degrees')
        sleep_ms(50)

    # rotate all clockwise
    a = 0
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot()
        sleep_ms(100)

    # rotate all anti clockwise
    a = 0
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot(fwd=False)
        sleep_ms(100)

    # random rings
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ringz.rand(randint(0,ringtotal - 1), min=minb, max=maxb)
        sleep_ms(randint(0,100))
    ringz.rand(min=minb, max=maxb)

    # rotate all clockwise
    a = 0
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot()
        sleep_ms(100)

    # rotate all anti clockwise
    a = 0
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot(fwd=False)
        sleep_ms(100)

    # fadeout
    for ring in range(ringtotal - 1, -1, -1):
        r = ringz.rings[ring][0][1][0]
        g = ringz.rings[ring][0][1][1]
        b = ringz.rings[ring][0][1][2]
        for step in range(max(r, g, b)):
            r = max(0, r - 1)
            g = max(0, g - 1)
            b = max(0, b - 1)
            ringz.set(ring,(r, g, b))
            sleep_ms(int(50 / sfac))

    cont = False    # exit

print('Fin')
ringz.set()
