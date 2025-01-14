from random import randint
from math import pi
from gc import collect
from json import dumps, loads
#from gc import collect

class PixRing():
    '''
    Cerates a NeoPixel Ring object

    Required:
        neopixels = a neopixel.NeoPixel() object
        ringmap   = a [list] giving the number of pixels in each ring
    Optional:
        limit     = default: 255
                    an int() or (tuple) specifiying a 'hard' maximum RGB
                    value that can be set for any pixel
        start     = default: 0
                    Index of the first pixel of the rings, if integer the rings
                    are assumed to follow each other; or a list can be supplied
                    giving the index number of the first pixel in each ring.
    '''
    
    ALL = None

    def __init__(self,neopixels,ringmap,limit=255,start=0):
        self._limit = self._rgbTuple(limit)
        self._np = neopixels
        self.rings = []
        n = start if type(start) is int else -1
        for r in range(len(ringmap)):
            self.rings.append([])
            n = n if type(start) is int else start[r]
            for p in range(ringmap[r]):
                self.rings[r].append([n,(0,0,0)])
                n += 1

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

    def _setNp(self,pix,val):
        # Set a pixel while applying limit & remember value
        # returns the value written
        newval = []
        for i in range(len(val)):
            newval.append(min(val[i],self._limit[i]))
        self._np[pix] = newval
        return newval

    def _angleToDecimal(self, pos, units):
        # convert inpot 'postion' to a decimal (0-1)
        # according to 'units', returns -1 on error
        if units[0:3] == 'deg':
            return float(pos / 360)
        elif units[0:3] == 'dec':
            return float(pos)
        elif units[0:3] == 'rad':
            return float(pos / (2 * pi))
        # we have a problem Jim.
        return -1
    
    def colorwheel(self,points=360,saturation=1,peak=255):
            # returns a colrwheel map object
        def hsv_to_rgb( h:scalar, s:scalar, v:scalar) -> tuple:
            if h == 1.0: h = 0.0
            i = int(h*6.0)
            f = h*6.0 - i
            w = int(v*( 1.0 - s) )
            q = int(v*( ( 1.0 - s * f) ) )
            t = int(v*( ( 1.0 - s * ( 1.0 - f ) ) ) )
            v = int(v)
            if i==0: return(v, t, w)
            if i==1: return(q, v, w)
            if i==2: return(w, v, t)
            if i==3: return(w, q, v)
            if i==4: return(t, w, v)
            if i==5: return(v, w, q)

        wheel = [[0,0,0]] * points
        for point in range(points):
            wheel[point] = hsv_to_rgb(point/points,saturation,peak)
        return wheel

    def set(self, rings=None, rgb=(0,0,0)):
        rgb = self._rgbTuple(rgb)
        rings = self._ringList(rings)
        for r in rings:
            for p in self.rings[r]:
                p[1] = self._setNp(p[0],rgb)
        self._np.write()
        collect()

    def pos(self, rings=None, rgb=(0,0,0), pos=0.0, units='degrees', fill=False):
        # WORK IN PROGRESS. SET TO CLOSEST (ANGULAR) PIXEL
        rgb = self._rgbTuple(rgb)
        rings = self._ringList(rings)
        pos = self._angleToDecimal(pos,units)
        if pos == -1:
            print('error: Unknown angle definition: {}'.format(units))
            return
        # reduce the decimal places and restrict range
        pos = round(float(max(0,min(1,pos))),3)
        for r in rings:
            rpos = int(len(self.rings[r]) * pos)
            self.rings[r][rpos][1] = self._setNp(self.rings[r][rpos][0],rgb)
            # TODO: add 'fill' function..
            #for p in self.rings[r] # but only up to 'rpos'..
            #    p[1] = self._setNp(p[0],rgb)
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
                p[1] = self._setNp(p[0],rgb)
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
                #print(p,self.rings[r][p][1],p[0],o[p])
                self.rings[r][p][1]  = self._setNp(self.rings[r][p][0],o[p])
                #was..
                #self._np[self.rings[r][p][0]] = o[p]
                #self.rings[r][p][1] = o[p]
        self._np.write()
        collect()

    def wheel(self, rings=None, pos=0, units='degrees'):
        rings = self._ringList(rings)
        pos = self._angleToDecimal(pos,units)
        for r in rings:
            for p in self.rings[r]:
                rgb = (
                    #randint(rmin[0],rmax[0]),
                    #randint(rmin[1],rmax[1]),
                    #randint(rmin[2],rmax[2]),
                    )
                p[1] = self._setNp(p[0],rgb)
        self._np.write()
        collect()

    def save(self):
        # Helper: dump the whole status.
        return dumps(self.rings)

    def load(self, json):
        # Helper: load whole status, apply the limit
        self.rings = loads(json)
        for p in self.rings:
            p[1] = self._setNp(p[0],p[1])
        self._np.write()
        collect()

#if __name__ == "__main__":
#    pass
