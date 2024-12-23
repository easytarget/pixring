from random import randint
from math import pi
from gc import collect
from json import dumps, loads

class PixRing():
    def __init__(self,pixels,ringmap,limit=255):
        self.limit = limit
        self._np = pixels
        self.rings = []
        n = 0
        for r in range(len(ringmap)):
            self.rings.append([])
            for p in range(ringmap[r]):
                self.rings[r].append([n,(0,0,0)])
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
                p[1] = rgb
        self._np.write()
        collect()

    def pos(self, rings=None, rgb=(0,0,0), pos=0.0, fill=False, units='degrees'):
        rgb = self._rgbTuple(rgb)
        rings = self._ringList(rings)
        if units[0:3] == 'deg':
            pos = float(pos / 360)
        elif units[0:3] == 'dec':
            pos = float(pos)
        elif units[0:3] == 'rad':
            pos = float(pos / (2 * pi))
        else:
            print('error: Unknown angle units: {}'.format(units))
            return
        pos = round(float(max(0,min(1,pos))),3)
        for r in rings:
            # Calculate nearest point
            rpos = int(len(self.rings[r]) * pos)
            #for p in self.rings[r]:
            #    self._np[p[0]] = rgb
            #    p[1] = rgb
            print(r,pos,rpos)
        #self._np.write()
        #collect()

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
                p[1] = rgb
        self._np.write()
        collect()

    def rot(self, rings=None, fwd=True):
        rings = self._ringList(rings)
        for r in rings:
            # record old data
            o = []
            for i in self.rings[r]:
                o.append(i[1])
            o = o[-1:] + o[:-1] if fwd else o[1:] + o[:1]
            for p in range(len(self.rings[r])):
                self._np[self.rings[r][p][0]] = o[p]
                self.rings[r][p][1] = o[p]
        self._np.write()
        collect()
        
    def save(self):
        return dumps(self.rings)
    
    def load(self, json):
        self.rings = loads(json)
        for p in self.rings:
            self._np(p[0],p[1])
        self._np.write()
        collect()

#if __name__ == "__main__":
#    pass
        ringz.set()
