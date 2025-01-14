'''
todo

Library:
ringlist == -1 for all rings (not None)
provide: pixrings.ALL = -1

Stop keeping a seperate value array.. ??

Colorwheel.. use maps for speed..

demo:
'Roll out a colorin a circular way.. (use to 'blank)'
'''


from pixrings import PixRing
from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms
from random import randint
from sys import exit

'''
    demo

    Important:
    Adjust the Pin and Ring Information below to match your setup!

'''

pix_pin = Pin(3)
num_pix = 124
np = NeoPixel(pix_pin, num_pix)


ringlist = [45,35,24,12,8]
ringtotal = len(ringlist)
ringz = PixRing(np,ringlist)
ringz.set()

# limits and spread
minb = 1
maxb = 16
sfac = 1  # spread factor
steptime = 6000

cont = True
wheel = ringz.colorwheel(180,saturation=1,peak=maxb)


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

    # random color changes
    end = ticks_ms() + steptime
    while ticks_ms() < end:
        ring = randint(0,ringtotal - 1)
        r = randint(minb,maxb)
        g = randint(minb,maxb)
        b = randint(minb,maxb)
        #r = max(minb,min(maxb, ringz.rings[ring][0][1][0] + randint(-sfac,sfac)))
        #g = max(minb,min(maxb, ringz.rings[ring][0][1][1] + randint(-sfac,sfac)))
        #b = max(minb,min(maxb, ringz.rings[ring][0][1][2] + randint(-sfac,sfac)))
        ringz.pos(ring,(r,g,b),pos=randint(0,359),units='degrees')

    # Clear: raw wipe demo
    # This bypasses the ringz methods, and writes to the pixels directly
    for a in range(num_pix):
        ringz._np[a] = (0,0,0)
        ringz._np.write()
        sleep_ms(5)

    # temp..
    n = 0
    for r in range(len(ringlist)):
        for p in range(ringlist[r]):
            ringz._np[n]=wheel[(int((len(wheel)/ringlist[r])*p)) % len(wheel)]
            n = n + 1
        ringz._np.write()
        sleep_ms(200)
        
    sleep_ms(500)

    # Build colorwheels from inside out then..
    # Colorwheels
    end = ticks_ms() + steptime
    while ticks_ms() < end:
        for a in range(len(wheel)):
            n = 0
            for r in range(len(ringlist)):
                for p in range(ringlist[r]):
                    ringz._np[n]=wheel[(int((len(wheel)/ringlist[r])*p)+a) % len(wheel)]
                    n = n + 1
            ringz._np.write()
    
    # Fast sweep clean
    for a in range(max(ringlist)*2):
        ringz.pos(None,(0,0,0),pos=a/(max(ringlist)*2),units='decimal')

    # Random spokes
    end = ticks_ms() + steptime
    while ticks_ms() < end:
        angle  = randint(0,359)
        ringz.pos(rgb=(randint(minb,maxb),randint(minb,maxb),randint(minb,maxb)),pos=angle,units='degrees')
        sleep_ms(50)

    # rotate all clockwise
    a = 0
    end = ticks_ms() + steptime
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot()
        sleep_ms(100)

    # random rings
    end = ticks_ms() + steptime
    while ticks_ms() < end:
        ringz.rand(randint(0,ringtotal - 1), min=minb, max=maxb)
        sleep_ms(randint(0,100))
    ringz.rand(min=minb, max=maxb)

    # rotate all anti clockwise
    a = 0
    end = ticks_ms() + steptime
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

    #cont = False    # exit

print('Fin')
ringz.set()
