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

import usb_hid
from board import SDA, SCL
from busio import I2C
from adafruit_hid.keyboard import Keyboard

from makbe.i2c_scanner import I2CScanner
from makbe.key_switch import KeySwitch
from makbe import k, KeyCode, TCA9555, m, mt, lt
from makbe.modeless_processor import ModelessProcessor


class KC(KeyCode):      # KeyCodeが頻出するので短縮形を作っておく
    pass


class Layer:
    QWERTY = 0
    LOWER = 1
    RAISE = 2
    FUNCS = 3


class Switches:
    """キースイッチ一覧
    このライブラリでは、Switchesクラスとして使用するキースイッチを全部列挙する
    """

    def __init__(self):
        self.esc = KeySwitch([
            k(KC.ESCAPE),
            k(KC.GRAVE),
            m(KC.L_SHIFT, KC.GRAVE)
        ])

        self.kb_q = KeySwitch([
            k(KC.KB_Q),
            m(KC.L_GUI, KC.KB_Q),
            k(KC.KB_1),
            k(KC.F1)
        ])
        self.kb_w = KeySwitch([
            k(KC.KB_W),
            m(KC.L_GUI, KC.KB_W),
            k(KC.KB_2),
            k(KC.F2)
        ])
        self.kb_e = KeySwitch([
            k(KC.KB_E),
            m(KC.L_GUI, KC.KB_E),
            k(KC.KB_3),
            k(KC.F3)
        ])
        self.kb_r = KeySwitch([
            k(KC.KB_R),
            m(KC.L_GUI, KC.KB_R),
            k(KC.KB_4),
            k(KC.F4)
        ])
        self.kb_t = KeySwitch([
            k(KC.KB_T),
            m(KC.L_GUI, KC.KB_T),
            k(KC.KB_5),
            k(KC.F5)
        ])
        self.kb_y = KeySwitch([
            k(KC.KB_Y),
            m(KC.L_GUI, KC.KB_Y),
            k(KC.KB_6),
            k(KC.F6)
        ])
        self.kb_u = KeySwitch([
            k(KC.KB_U),
            m(KC.L_GUI, KC.KB_U),
            k(KC.KB_7),
            k(KC.F7)
        ])
        self.kb_i = KeySwitch([
            k(KC.KB_I),
            m(KC.L_GUI, KC.KB_I),
            k(KC.KB_8),
            k(KC.F8)
        ])
        self.kb_o = KeySwitch([
            k(KC.KB_O),
            m(KC.L_GUI, KC.KB_O),
            k(KC.KB_9),
            k(KC.F9)
        ])
        self.kb_p = KeySwitch([
            k(KC.KB_P),
            m(KC.L_GUI, KC.KB_P),
            k(KC.KB_0),
            k(KC.F10)
        ])
        self.minus = KeySwitch([
            k(KC.MINUS),
            k(KC.EQUAL),
            k(KC.EQUAL),
            k(KC.F11)
        ])
        self.back_space = KeySwitch([
            k(KC.BACK_SPACE),
            m(KC.L_GUI, KC.BACK_SPACE),
            k(KC.DELETE),
            k(KC.F12)
        ])

        self.tab = KeySwitch([
            k(KC.TAB),
            m(KC.L_GUI, KC.TAB)
        ])
        self.kb_a = KeySwitch([
            k(KC.KB_A),
            m(KC.L_GUI, KC.KB_A)
        ])
        self.kb_s = KeySwitch([
            k(KC.KB_S),
            m(KC.L_GUI, KC.KB_S)
        ])
        self.kb_d = KeySwitch([
            k(KC.KB_D),
            m(KC.L_GUI, KC.KB_D)
        ])
        self.kb_f = KeySwitch([
            k(KC.KB_F),
            m(KC.L_GUI, KC.KB_F)
        ])
        self.kb_g = KeySwitch([
            k(KC.KB_G),
            m(KC.L_GUI, KC.KB_G)
        ])
        self.kb_h = KeySwitch([
            k(KC.KB_H),
            m(KC.L_GUI, KC.KB_H)
        ])
        self.kb_j = KeySwitch([
            k(KC.KB_J),
            m(KC.L_GUI, KC.KB_J)
        ])
        self.kb_k = KeySwitch([
            k(KC.KB_K),
            m(KC.L_GUI, KC.KB_K)
        ])
        self.kb_l = KeySwitch([
            k(KC.KB_L),
            m(KC.L_GUI, KC.KB_L)
        ])
        self.semi_colon = KeySwitch([
            k(KC.SEMI_COLON),
            m(KC.L_GUI, KC.SEMI_COLON)
        ])
        self.enter = KeySwitch([
            k(KC.ENTER),
            m(KC.L_GUI, KC.ENTER)
        ])

        self.l_shift = KeySwitch([
            k(KC.L_SHIFT)
        ])
        self.kb_z = KeySwitch([
            k(KC.KB_Z),
            m(KC.L_GUI, KC.KB_Z)
        ])
        self.kb_x = KeySwitch([
            k(KC.KB_X),
            m(KC.L_GUI, KC.KB_X)
        ])
        self.kb_c = KeySwitch([
            k(KC.KB_C),
            m(KC.L_GUI, KC.KB_C)
        ])
        self.kb_v = KeySwitch([
            k(KC.KB_V),
            m(KC.L_GUI, KC.KB_V)
        ])
        self.kb_b = KeySwitch([
            k(KC.KB_B),
            m(KC.L_GUI, KC.KB_B)
        ])
        self.kb_n = KeySwitch([
            k(KC.KB_N),
            m(KC.L_GUI, KC.KB_N)
        ])
        self.kb_m = KeySwitch([
            k(KC.KB_M),
            m(KC.L_GUI, KC.KB_M)
        ])
        self.comma = KeySwitch([
            k(KC.COMMA),
            k(KC.L_BRACKET),
            m(KC.R_SHIFT, KC.L_BRACKET)
        ])
        self.dot = KeySwitch([
            k(KC.DOT),
            k(KC.R_BRACKET),
            m(KC.R_SHIFT, KC.R_BRACKET)
        ])
        self.up = KeySwitch([
            k(KC.UP),
            m(KC.L_GUI, KC.UP),
            k(KC.PAGE_UP)
        ])
        self.slash = KeySwitch([
            k(KC.SLASH),
            k(KC.BACK_SLASH),
            k(KC.BACK_SLASH)
        ])

        self.l_ctrl = KeySwitch([
            k(KC.L_CTRL)
        ])
        self.l_gui = KeySwitch([
            k(KC.L_GUI)
        ])
        self.delete = KeySwitch([
            k(KC.DELETE)
        ])
        self.l_alt = KeySwitch([
            mt(KC.L_ALT, KC.LANG_2)
        ])
        self.l_space = KeySwitch([
            lt(Layer.LOWER, KC.SPACE)
        ])
        self.r_space = KeySwitch([
            mt(KC.R_SHIFT, KC.SPACE)
        ])
        self.r_gui = KeySwitch([
            lt(Layer.RAISE, KC.LANG_1)
        ])
        self.r_alt = KeySwitch([
            k(KC.R_ALT)
        ])
        self.left = KeySwitch([
            k(KC.LEFT),
            m(KC.L_GUI, KC.LEFT),
            k(KC.HOME)
        ])
        self.down = KeySwitch([
            k(KC.DOWN),
            m(KC.L_GUI, KC.DOWN),
            k(KC.PAGE_DOWN)
        ])
        self.right = KeySwitch([
            k(KC.RIGHT),
            m(KC.L_GUI, KC.RIGHT),
            k(KC.END)
        ])


class Column13ansi:
    """例としてColumn13のansi配列を実装している
    """

    def __init__(self):
        """キーボードの初期化
        キースイッチクラスタを生成し、I2CScannerを使うのでI/Oエクスパンダにそれを割り当ててて、
        とりあえず、ModelessProcessorで処理するようにしている
        """
        # スイッチとI/Oエクスパンダのリストを生成
        self.sw = Switches()
        self.expanders = []

        # キーの割り当て、1つ目
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

        # キーの割り当て、2つ目
        expander = TCA9555(0x01)
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

        # キーの割り当て、3つ目
        expander = TCA9555(0x02)
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

        # キーの割り当て、4つ目
        expander = TCA9555(0x03)
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
        expander.assign(12, self.sw.down)
        expander.assign(13, self.sw.right)
        self.expanders.append(expander)

        # I2Cマスタの生成
        i2c = I2C(SCL, SDA)
        while not i2c.try_lock():
            pass

        # プロセッサ（とりあえずModelessProcessor）の生成
        kbd = Keyboard(usb_hid.devices)
        proc = ModelessProcessor(kbd)

        # スキャナの生成
        self.scanner = I2CScanner(self.expanders, i2c, proc)
