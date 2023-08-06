"""
Drivers for electricdollarstore I2C parts
"""
import struct
import time

class Dig2:
    """ DIG2 is a 2-digit 7-segment LED display """

    def __init__(self, i2, a = 0x14):
        self.i2 = i2
        self.a = a

    def raw(self, b0, b1):
        """ Set all 8 segments from the bytes b0 and b1 """ 
        self.i2.regwr(self.a, 0, b0, b1)

    def hex(self, b):
        """ Display a hex number 0-0xff """
        self.i2.regwr(self.a, 1, b)

    def dec(self, b):
        """ Display a decimal number 00-99 """
        self.i2.regwr(self.a, 2, b)

    def dp(self, p0, p1):
        """ Set the state the decimal point indicators """
        self.i2.regwr(self.a, 3, (p1 << 1) | p0)

    def brightness(self, b):
        """ Set the brightness from 0 (off) to 255 (maximum) """
        self.i2.regwr(self.a, 4, b)

class LED:
    """ LED is an RGB LED """
    def __init__(self, i2, a = 0x08):
        self.i2 = i2
        self.a = a

    def rgb(self, r, g, b, t = 0):
        """
        Set the color to (r,g,b). Each is a byte 0-255.
        If t is nonzero, the change happens over t/30 seconds.
        For example if t is 15 the color fades over a half-second.
        """
        if t == 0:
            self.i2.start(self.a, 0)
            self.i2.write(bytes((0, r, g, b)))
            self.i2.stop()
        else:
            self.i2.start(self.a, 0)
            self.i2.write(bytes((1, r, g, b, t)))
            self.i2.stop()
        
    def hex(self, hhh, t = 0):
        """
        Set the color to hhh, a 24-bit RGB color.
        If t is nonzero, the change happens over t/30 seconds.
        For example if t is 15 the color fades over a half-second.
        """
        r = (hhh >> 16) & 0xff
        g = (hhh >> 8) & 0xff
        b = hhh & 0xff
        self.rgb(r, g, b, t)

class Pot:
    """ POT is an analog knob potentiometer """
    def __init__(self, i2, a = 0x28):
        self.i2 = i2
        self.a = a

    def raw(self):
        """
        Return the current knob rotation as a 16-bit integer.
        """
        return self.i2.regrd(self.a, 0, "H")

    def rd(self, r):
        """
        Return the current knob rotation, scaled to the range 0 .. r
        inclusive. For example rd(100) returns a value in the range 0 to 100.
        """
        return self.i2.regrd(self.a, r)

class Beep:
    """ BEEP is a beeper """
    def __init__(self, i2, a = 0x30):
        self.i2 = i2
        self.a = a

    def beep(self, dur, note):
        """
        Play a note. 
        dur is the duration in centi-seconds.
        note is a MIDI note in the range 21-127 inclusive.
        """
        self.i2.regwr(self.a, dur, note)

class Remote:
    """ REMOTE is a NEC IR code receiver / decoder """
    def __init__(self, i2, a = 0x60):
        self.i2 = i2
        self.a = a

    def key(self):
        """
        For the electricdollarstore IR transmitter.
        If there is a code in the queue, return its character code.
        The layout of the remote is
            
             p     c     n
             <     >    ' '
             -     +     =
             0     %     &
             1     2     3
             4     5     6
             7     8     9

        If there is no IR code in the queue, return None.
        """
        while True:
            r = self.i2.regrd(self.a, 0)
            if r != 0:
                return chr(r)

    def raw(self):
        """
        If there is a code in the queue, return a tuple containing the four-byte code,
        and a timestamp.
        If there is no IR code in the queue, return None.
        """

        r = self.i2.regrd(self.a, 1, "4BH")
        if r[:4] != (0xff, 0xff, 0xff, 0xff):
            age_in_ms = r[4]
            return (r[:4], time.time() - age_in_ms * .001)
        else:
            return None

class Temp:
    """ TEMP is a LM75B temperature sesnor """
    def __init__(self, i2, a = 0x48):
        self.i2 = i2
        self.a = a

    def reg(self, r):
        return self.i2.regrd(self.a, r, ">h")
        
    def read(self):
        """ Return the current temperature in Celsius """
        return (self.reg(0) >> 5) * 0.125

class EPROM:
    """ EPROM is a CAT24C512 512 Kbit (64 Kbyte) flash memory """
    def __init__(self, i2, a = 0x50):
        self.i2 = i2
        self.a = a

    def write(self, addr, data):
        """ Write data to EPROM, starting at address addr """
        for i in range(0, len(data), 128):
            self.i2.start(self.a, 0)
            self.i2.write(struct.pack(">H", addr + i))
            self.i2.write(data[i:i + 128])
            self.i2.stop()
            while self.i2.start(self.a, 0) == False:
                pass
        
    def read(self, addr, n):
        """ Read n bytes from the EPROM, starting at address addr """
        self.i2.start(self.a, 0)
        self.i2.write(struct.pack(">H", addr))
        self.i2.start(self.a, 1)
        r = self.i2.read(n)
        self.i2.stop()
        return r
        self.i2.stop()

class CLOCK:
    """ CLOCK is a HT1382 I2C/3-Wire Real Time Clock with a 32 kHz crystal """
    def __init__(self, i2, a = 0x68):
        self.i2 = i2
        self.a = a
        
        self.dump()
        self.i2.regwr(self.a, 7, 0)
        self.i2.regwr(self.a, 0, 0)
        self.dump()

        while 1:
            self.dump()
            time.sleep(1)

    def dump(self):
        self.i2.start(self.a, 0)
        self.i2.write([0])
        self.i2.stop()
        self.i2.start(self.a, 1)
        print(list(self.i2.read(16)))
        self.i2.stop()

    def read(self):
        pass
