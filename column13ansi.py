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
from board import *
from busio import I2C
import usb_hid
from adafruit_hid.keyboard import Keyboard
from makbe import I2CScanner, KeySwitch, k, KeyCode, TCA9555
from makbe.modeless_processor import ModelessProcessor


class Switches:

    def __init__(self):
        self.esc = KeySwitch(k(KeyCode.ESCAPE))
        self.kb_q = KeySwitch(k(KeyCode.KB_Q))
        self.kb_w = KeySwitch(k(KeyCode.KB_W))
        self.kb_e = KeySwitch(k(KeyCode.KB_E))
        self.kb_r = KeySwitch(k(KeyCode.KB_R))
        self.kb_t = KeySwitch(k(KeyCode.KB_T))
        self.kb_y = KeySwitch(k(KeyCode.KB_Y))
        self.kb_u = KeySwitch(k(KeyCode.KB_U))
        self.kb_i = KeySwitch(k(KeyCode.KB_I))
        self.kb_o = KeySwitch(k(KeyCode.KB_O))
        self.kb_p = KeySwitch(k(KeyCode.KB_P))
        self.minus = KeySwitch(k(KeyCode.MINUS))
        self.back_space = KeySwitch(k(KeyCode.BACK_SPACE))
        self.tab = KeySwitch(k(KeyCode.TAB))
        self.kb_a = KeySwitch(k(KeyCode.KB_A))
        self.kb_s = KeySwitch(k(KeyCode.KB_S))
        self.kb_d = KeySwitch(k(KeyCode.KB_D))
        self.kb_f = KeySwitch(k(KeyCode.KB_F))
        self.kb_g = KeySwitch(k(KeyCode.KB_G))
        self.kb_h = KeySwitch(k(KeyCode.KB_H))
        self.kb_j = KeySwitch(k(KeyCode.KB_J))
        self.kb_k = KeySwitch(k(KeyCode.KB_K))
        self.kb_l = KeySwitch(k(KeyCode.KB_L))
        self.semi_colon = KeySwitch(k(KeyCode.SEMI_COLON))
        self.enter = KeySwitch(k(KeyCode.ENTER))
        self.l_shift = KeySwitch(k(KeyCode.L_SHIFT))
        self.kb_z = KeySwitch(k(KeyCode.KB_Z))
        self.kb_x = KeySwitch(k(KeyCode.KB_X))
        self.kb_c = KeySwitch(k(KeyCode.KB_S))
        self.kb_v = KeySwitch(k(KeyCode.KB_V))
        self.kb_b = KeySwitch(k(KeyCode.KB_B))
        self.kb_n = KeySwitch(k(KeyCode.KB_N))
        self.kb_m = KeySwitch(k(KeyCode.KB_M))
        self.comma = KeySwitch(k(KeyCode.COMMA))
        self.dot = KeySwitch(k(KeyCode.DOT))
        self.up = KeySwitch(k(KeyCode.UP))
        self.slash = KeySwitch(k(KeyCode.SLASH))
        self.l_ctrl = KeySwitch(k(KeyCode.L_CTRL))
        self.l_gui = KeySwitch(k(KeyCode.L_GUI))
        self.delete = KeySwitch(k(KeyCode.DELETE))
        self.l_alt = KeySwitch(k(KeyCode.L_ALT))
        self.l_space = KeySwitch(k(KeyCode.SPACE))
        self.r_space = KeySwitch(k(KeyCode.SPACE))
        self.r_gui = KeySwitch(k(KeyCode.R_GUI))
        self.r_alt = KeySwitch(k(KeyCode.R_ALT))
        self.left = KeySwitch(k(KeyCode.LEFT))
        self.down = KeySwitch(k(KeyCode.DOWN))
        self.right = KeySwitch(k(KeyCode.RIGHT))


class Column13ansi:

    def __init__(self):
        self.sw = Switches()
        self.expanders = []

        expander = TCA9555(0x00)
        expander.assign(0, self.sw.esc)
        expander.assign(1, self.sw.kb_q)
        expander.assign(2, self.sw.kb_w)
        expander.assign(3, self.sw.kb_e)
        expander.assign(4, self.sw.kb_r)
        expander.assign(5, self.sw.kb_t)
        expander.assign(8, self.sw.tab)
        expander.assign(9, self.sw.kb_a)
        expander.assign(10, self.sw.kb_s)
        expander.assign(11, self.sw.kb_d)
        expander.assign(12, self.sw.kb_f)
        expander.assign(13, self.sw.kb_g)
        self.expanders.append(expander)

        expander = TCA9555(0x00)
        expander.assign(0, self.sw.kb_y)
        expander.assign(1, self.sw.kb_u)
        expander.assign(2, self.sw.kb_i)
        expander.assign(3, self.sw.kb_o)
        expander.assign(4, self.sw.kb_p)
        expander.assign(5, self.sw.minus)
        expander.assign(6, self.sw.back_space)
        expander.assign(8, self.sw.kb_h)
        expander.assign(9, self.sw.kb_j)
        expander.assign(10, self.sw.kb_k)
        expander.assign(11, self.sw.kb_l)
        expander.assign(12, self.sw.semi_colon)
        expander.assign(13, self.sw.enter)
        self.expanders.append(expander)

        expander = TCA9555(0x00)
        expander.assign(0, self.sw.l_shift)
        expander.assign(1, self.sw.kb_z)
        expander.assign(2, self.sw.kb_x)
        expander.assign(3, self.sw.kb_c)
        expander.assign(4, self.sw.kb_v)
        expander.assign(5, self.sw.kb_b)
        expander.assign(8, self.sw.l_ctrl)
        expander.assign(9, self.sw.l_gui)
        expander.assign(10, self.sw.delete)
        expander.assign(11, self.sw.l_alt)
        expander.assign(12, self.sw.l_space)
        self.expanders.append(expander)

        expander = TCA9555(0x00)
        expander.assign(0, self.sw.kb_n)
        expander.assign(1, self.sw.kb_m)
        expander.assign(2, self.sw.comma)
        expander.assign(3, self.sw.dot)
        expander.assign(4, self.sw.up)
        expander.assign(5, self.sw.slash)
        expander.assign(8, self.sw.r_space)
        expander.assign(9, self.sw.r_gui)
        expander.assign(10, self.sw.r_alt)
        expander.assign(11, self.sw.left)
        expander.assign(12, self.sw.dot)
        expander.assign(13, self.sw.right)
        self.expanders.append(expander)

        i2c = I2C(SDA, SCL)
        while not i2c.try_lock():
            pass

        kbd = Keyboard(usb_hid.devices)
        self.scanner = I2CScanner(self.expanders, i2c, ModelessProcessor(kbd))

    def scan(self):
        self.scanner.scan()