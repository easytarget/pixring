from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms
from random import randint
from gc import collect

class pixRing():
    def __init__(self,pixels,ringmap):
        self._np = pixels
        self.rings = []
        n = 0
        for r in range(len(ringmap)):
            self.rings.append([])
            for p in range(ringmap[r]):
                self.rings[r].append([n,0,0,0])
                n += 1
        if n != self._np.n:
            self._pp('warning: pixel count missmatch')

    def _pp(self, text):
        print(text)

    def _rgbTuple(self, rgb):
        if type(rgb) is int:
            r = g = b = int(rgb)
        else:
            r, g, b = rgb
        return (r, g, b)

    def _ringList(self, rings):
        rings = range(len(self.rings)) if rings is None else rings
        return [rings] if type(rings) is int else rings

    def set(self, rings=None, rgb=(0,0,0)):
        rgb = self._rgbTuple(rgb)
        rings = self._ringList(rings)
        for r in rings:
            for p in self.rings[r]:
                self._np[p[0]] = rgb
                p[1], p[2], p[3] = rgb
        self._np.write()
        collect()

    def rand(self, rings=None, min=(0,0,0), max=(255,255,255)):
        rmin = self._rgbTuple(min)
        rmax = self._rgbTuple(max)
        rings = self._ringList(rings)
        for r in rings:
            for p in self.rings[r]:
                rgb = (
                    randint(rmin[0],rmax[0]),
                    randint(rmin[1],rmax[1]),
                    randint(rmin[2],rmax[2]),
                    )
                self._np[p[0]] = rgb
                p[1], p[2], p[3] = rgb
        self._np.write()
        collect()

    def rot(self, rings=None, fwd=True):
        rings = self._ringList(rings)
        for r in rings:
            # record old data
            o = []
            for i in self.rings[r]:
                o.append((i[1],i[2],i[3]))
            o = o[-1:] + o[:-1] if fwd else o[1:] + o[:1]
            for p in range(len(self.rings[r])):
                self._np[self.rings[r][p][0]] = o[p]
                self.rings[r][p][1] = o[p][0]
                self.rings[r][p][2] = o[p][1]
                self.rings[r][p][3] = o[p][2]
        self._np.write()
        collect()

#if __name__ == "__main__":
'''
    demo
'''

num_pix = 124
np = NeoPixel(Pin(26), num_pix)
'''
np_i = NeoPixel(machine.Pin(12), 1)
pwr_i = Pin(11, Pin.OUT)
pwr_i.off()
'''


ringlist = [45,35,24,12,8]
ringtotal = len(ringlist)
ringz = pixRing(np,ringlist)

# limits and spread
minb = 1
maxb = 12
sfac = 1  # spread factor

ringz.set()
cont = True

while cont:
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

    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ringz.set(randint(0,ringtotal - 1),(randint(minb,maxb),randint(minb,maxb),randint(minb,maxb)))
        sleep_ms(randint(0,100))

    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ring = randint(0,ringtotal - 1)
        r = max(minb,min(maxb, ringz.rings[ring][0][1] + randint(-sfac,sfac)))
        g = max(minb,min(maxb, ringz.rings[ring][0][2] + randint(-sfac,sfac)))
        b = max(minb,min(maxb, ringz.rings[ring][0][3] + randint(-sfac,sfac)))
        ringz.set(ring,(r,g,b))


    end = ticks_ms() + 3000
    while ticks_ms() < end:
        ringz.rand(randint(0,ringtotal - 1), min=minb, max=maxb)
        sleep_ms(randint(0,100))
    ringz.rand(min=minb, max=maxb)

    a = 0
    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot()
        sleep_ms(100)

    end = ticks_ms() + 3000
    while ticks_ms() < end:
        a = (a + 1) % ringtotal
        ringz.rot(fwd=False)
        sleep_ms(100)

    for ring in range(ringtotal - 1, -1, -1):
        r = ringz.rings[ring][0][1]
        g = ringz.rings[ring][0][2]
        b = ringz.rings[ring][0][3]
        for step in range(max(r, g, b)):
            r = max(0, r - 1)
            g = max(0, g - 1)
            b = max(0, b - 1)
            ringz.set(ring,(r, g, b))
            sleep_ms(int(50 / sfac))

    #cont = False    # exit

print('Fin')
ringz.set()
