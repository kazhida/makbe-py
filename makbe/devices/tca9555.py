# MIT License
#
# Copyright (c) 2021 Kazuyuki HIDA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .. import Device, KeySwitch, dummy_switch


class TCA9555(Device):

    def __init__(self, dev_addr: int):
        self.dev_addr = dev_addr
        self.switches = []
        for i in range(16):
            self.switches.append(dummy_switch())

    def init_device(self, i2c) -> bool:
        i2c.writeto(self.dev_addr, bytes([0x06, 0xFF]), True)
        i2c.writeto(self.dev_addr, bytes([0x07, 0xFF]), True)
        return True

    def read_device(self, i2c) -> [bool]:
        i2c.writeto(self.dev_addr, bytes([0x00]), False)
        buffer = bytearray(2)
        i2c.readfrom_into(self.dev_addr, buffer)
        result = []
        for i, b in enumerate(buffer):
            for p in range(8):
                mask = 1 << p
                if buffer[i] & mask != 0:
                    result.append(True)
                else:
                    result.append(False)
        return result

    def assign(self, pin: int, switch: KeySwitch):
        self.switches[pin] = switch

    def switch(self, pin: int) -> KeySwitch:
        return self.switches[pin]
