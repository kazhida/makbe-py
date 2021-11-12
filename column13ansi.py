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
from makbe import kc, TCA9555, mc, mt, KeyCode, lt
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
            kc(KC.ESCAPE),
            kc(KC.GRAVE),
            mc(KC.L_SHIFT, KC.GRAVE)
        ])

        self.kb_q = KeySwitch([
            kc(KC.KB_Q),
            mc(KC.L_GUI, KC.KB_Q),
            kc(KC.KB_1),
            kc(KC.F1)
        ])
        self.kb_w = KeySwitch([
            kc(KC.KB_W),
            mc(KC.L_GUI, KC.KB_W),
            kc(KC.KB_2),
            kc(KC.F2)
        ])
        self.kb_e = KeySwitch([
            kc(KC.KB_E),
            mc(KC.L_GUI, KC.KB_E),
            kc(KC.KB_3),
            kc(KC.F3)
        ])
        self.kb_r = KeySwitch([
            kc(KC.KB_R),
            mc(KC.L_GUI, KC.KB_R),
            kc(KC.KB_4),
            kc(KC.F4)
        ])
        self.kb_t = KeySwitch([
            kc(KC.KB_T),
            mc(KC.L_GUI, KC.KB_T),
            kc(KC.KB_5),
            kc(KC.F5)
        ])
        self.kb_y = KeySwitch([
            kc(KC.KB_Y),
            mc(KC.L_GUI, KC.KB_Y),
            kc(KC.KB_6),
            kc(KC.F6)
        ])
        self.kb_u = KeySwitch([
            kc(KC.KB_U),
            mc(KC.L_GUI, KC.KB_U),
            kc(KC.KB_7),
            kc(KC.F7)
        ])
        self.kb_i = KeySwitch([
            kc(KC.KB_I),
            mc(KC.L_GUI, KC.KB_I),
            kc(KC.KB_8),
            kc(KC.F8)
        ])
        self.kb_o = KeySwitch([
            kc(KC.KB_O),
            mc(KC.L_GUI, KC.KB_O),
            kc(KC.KB_9),
            kc(KC.F9)
        ])
        self.kb_p = KeySwitch([
            kc(KC.KB_P),
            mc(KC.L_GUI, KC.KB_P),
            kc(KC.KB_0),
            kc(KC.F10)
        ])
        self.minus = KeySwitch([
            kc(KC.MINUS),
            kc(KC.EQUAL),
            kc(KC.EQUAL),
            kc(KC.F11)
        ])
        self.back_space = KeySwitch([
            kc(KC.BACK_SPACE),
            mc(KC.L_GUI, KC.BACK_SPACE),
            kc(KC.DELETE),
            kc(KC.F12)
        ])

        self.tab = KeySwitch([
            kc(KC.TAB),
            mc(KC.L_GUI, KC.TAB)
        ])
        self.kb_a = KeySwitch([
            kc(KC.KB_A),
            mc(KC.L_GUI, KC.KB_A)
        ])
        self.kb_s = KeySwitch([
            kc(KC.KB_S),
            mc(KC.L_GUI, KC.KB_S)
        ])
        self.kb_d = KeySwitch([
            kc(KC.KB_D),
            mc(KC.L_GUI, KC.KB_D)
        ])
        self.kb_f = KeySwitch([
            kc(KC.KB_F),
            mc(KC.L_GUI, KC.KB_F)
        ])
        self.kb_g = KeySwitch([
            kc(KC.KB_G),
            mc(KC.L_GUI, KC.KB_G)
        ])
        self.kb_h = KeySwitch([
            kc(KC.KB_H),
            mc(KC.L_GUI, KC.KB_H)
        ])
        self.kb_j = KeySwitch([
            kc(KC.KB_J),
            mc(KC.L_GUI, KC.KB_J)
        ])
        self.kb_k = KeySwitch([
            kc(KC.KB_K),
            mc(KC.L_GUI, KC.KB_K)
        ])
        self.kb_l = KeySwitch([
            kc(KC.KB_L),
            mc(KC.L_GUI, KC.KB_L)
        ])
        self.semi_colon = KeySwitch([
            kc(KC.SEMI_COLON),
            mc(KC.L_GUI, KC.SEMI_COLON)
        ])
        self.enter = KeySwitch([
            kc(KC.ENTER),
            mc(KC.L_GUI, KC.ENTER)
        ])

        self.l_shift = KeySwitch([
            kc(KC.L_SHIFT)
        ])
        self.kb_z = KeySwitch([
            kc(KC.KB_Z),
            mc(KC.L_GUI, KC.KB_Z)
        ])
        self.kb_x = KeySwitch([
            kc(KC.KB_X),
            mc(KC.L_GUI, KC.KB_X)
        ])
        self.kb_c = KeySwitch([
            kc(KC.KB_C),
            mc(KC.L_GUI, KC.KB_C)
        ])
        self.kb_v = KeySwitch([
            kc(KC.KB_V),
            mc(KC.L_GUI, KC.KB_V)
        ])
        self.kb_b = KeySwitch([
            kc(KC.KB_B),
            mc(KC.L_GUI, KC.KB_B)
        ])
        self.kb_n = KeySwitch([
            kc(KC.KB_N),
            mc(KC.L_GUI, KC.KB_N)
        ])
        self.kb_m = KeySwitch([
            kc(KC.KB_M),
            mc(KC.L_GUI, KC.KB_M)
        ])
        self.comma = KeySwitch([
            kc(KC.COMMA),
            kc(KC.L_BRACKET),
            mc(KC.R_SHIFT, KC.L_BRACKET)
        ])
        self.dot = KeySwitch([
            kc(KC.DOT),
            kc(KC.R_BRACKET),
            mc(KC.R_SHIFT, KC.R_BRACKET)
        ])
        self.up = KeySwitch([
            kc(KC.UP),
            mc(KC.L_GUI, KC.UP),
            kc(KC.PAGE_UP)
        ])
        self.slash = KeySwitch([
            kc(KC.SLASH),
            kc(KC.BACK_SLASH),
            kc(KC.BACK_SLASH)
        ])

        self.l_ctrl = KeySwitch([
            kc(KC.L_CTRL)
        ])
        self.l_gui = KeySwitch([
            kc(KC.L_GUI)
        ])
        self.delete = KeySwitch([
            kc(KC.DELETE)
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
            kc(KC.R_ALT)
        ])
        self.left = KeySwitch([
            kc(KC.LEFT),
            mc(KC.L_GUI, KC.LEFT),
            kc(KC.HOME)
        ])
        self.down = KeySwitch([
            kc(KC.DOWN),
            mc(KC.L_GUI, KC.DOWN),
            kc(KC.PAGE_DOWN)
        ])
        self.right = KeySwitch([
            kc(KC.RIGHT),
            mc(KC.L_GUI, KC.RIGHT),
            kc(KC.END)
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
