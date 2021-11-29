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
from board import GP4, GP5
from busio import I2C
from adafruit_hid.keyboard import Keyboard

from makbe.i2c_scanner import I2CScanner
from makbe.key_switch import KeySwitch
from makbe import kc, TCA9555, mc, mt, KeyCode, lt, trans, la
from makbe.layered_processor import LayeredProcessor
from makbe.wrapped_kbd import WrappedKeyboard


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
            mc(KC.L_SHIFT, KC.GRAVE),
            trans()
        ])

        self.kb_1 = KeySwitch([
            kc(KC.KB_1),
            mc(KC.L_GUI, KC.KB_1),
            mc(KC.L_SHIFT, KC.KB_1),
            kc(KC.F1)
        ])
        self.kb_2 = KeySwitch([
            kc(KC.KB_2),
            mc(KC.L_GUI, KC.KB_2),
            mc(KC.L_SHIFT, KC.KB_2),
            kc(KC.F2)
        ])
        self.kb_3 = KeySwitch([
            kc(KC.KB_3),
            mc(KC.L_GUI, KC.KB_3),
            mc(KC.L_SHIFT, KC.KB_3),
            kc(KC.F3)
        ])
        self.kb_4 = KeySwitch([
            kc(KC.KB_4),
            mc(KC.L_GUI, KC.KB_4),
            mc(KC.L_SHIFT, KC.KB_4),
            kc(KC.F4)
        ])
        self.kb_5 = KeySwitch([
            kc(KC.KB_5),
            mc(KC.L_GUI, KC.KB_5),
            mc(KC.L_SHIFT, KC.KB_5),
            kc(KC.F5)
        ])
        self.kb_6 = KeySwitch([
            kc(KC.KB_6),
            mc(KC.L_GUI, KC.KB_6),
            mc(KC.L_SHIFT, KC.KB_6),
            kc(KC.F6)
        ])
        self.kb_7 = KeySwitch([
            kc(KC.KB_7),
            mc(KC.L_GUI, KC.KB_7),
            mc(KC.L_SHIFT, KC.KB_7),
            kc(KC.F7)
        ])
        self.kb_8 = KeySwitch([
            kc(KC.KB_8),
            mc(KC.L_GUI, KC.KB_8),
            mc(KC.L_SHIFT, KC.KB_8),
            kc(KC.F8)
        ])
        self.kb_9 = KeySwitch([
            kc(KC.KB_9),
            mc(KC.L_GUI, KC.KB_9),
            mc(KC.L_SHIFT, KC.KB_9),
            kc(KC.F9)
        ])
        self.kb_0 = KeySwitch([
            kc(KC.KB_0),
            mc(KC.L_GUI, KC.KB_0),
            mc(KC.L_SHIFT, KC.KB_0),
            kc(KC.F10)
        ])
        self.minus = KeySwitch([
            kc(KC.MINUS),
            mc(KC.L_GUI, KC.MINUS),
            mc(KC.L_SHIFT, KC.MINUS),
            kc(KC.F11)
        ])
        self.equal = KeySwitch([
            kc(KC.EQUAL),
            mc(KC.L_GUI, KC.EQUAL),
            mc(KC.L_SHIFT, KC.EQUAL),
            kc(KC.F12)
        ])
        self.back_space = KeySwitch([
            kc(KC.BACK_SPACE),
            mc(KC.L_GUI, KC.BACK_SPACE),
            mc(KC.L_SHIFT, KC.BACK_SPACE),
            kc(KC.DELETE)
        ])

        self.tab = KeySwitch([
            kc(KC.TAB),
            mc(KC.L_GUI, KC.TAB),
            mc(KC.L_SHIFT, KC.TAB),
            trans()
        ])
        self.kb_q = KeySwitch([
            kc(KC.KB_Q),
            mc(KC.L_GUI, KC.KB_Q),
            mc(KC.L_SHIFT, KC.KB_Q),
            mc(KC.L_ALT, KC.LEFT)
        ])
        self.kb_w = KeySwitch([
            kc(KC.KB_W),
            mc(KC.L_GUI, KC.KB_W),
            mc(KC.L_SHIFT, KC.KB_W),
            mc(KC.L_ALT, KC.RIGHT)
        ])
        self.kb_e = KeySwitch([
            kc(KC.KB_E),
            mc(KC.L_GUI, KC.KB_E),
            mc(KC.L_SHIFT, KC.KB_E),
            kc(KC.UP)
        ])
        self.kb_r = KeySwitch([
            kc(KC.KB_R),
            mc(KC.L_GUI, KC.KB_R),
            mc(KC.L_SHIFT, KC.KB_R),
            kc(KC.PAGE_UP)
        ])
        self.kb_t = KeySwitch([
            kc(KC.KB_T),
            mc(KC.L_GUI, KC.KB_T),
            mc(KC.L_SHIFT, KC.KB_T),
            trans()
        ])
        self.kb_y = KeySwitch([
            kc(KC.KB_Y),
            mc(KC.L_GUI, KC.KB_Y),
            mc(KC.L_SHIFT, KC.KB_Y),
            trans()
        ])
        self.kb_u = KeySwitch([
            kc(KC.KB_U),
            mc(KC.L_GUI, KC.KB_U),
            mc(KC.L_SHIFT, KC.KB_U),
            trans()
        ])
        self.kb_i = KeySwitch([
            kc(KC.KB_I),
            mc(KC.L_GUI, KC.KB_I),
            mc(KC.L_SHIFT, KC.KB_I),
            trans()
        ])
        self.kb_o = KeySwitch([
            kc(KC.KB_O),
            mc(KC.L_GUI, KC.KB_O),
            mc(KC.L_SHIFT, KC.KB_O),
            trans()
        ])
        self.kb_p = KeySwitch([
            kc(KC.KB_P),
            mc(KC.L_GUI, KC.KB_P),
            mc(KC.L_SHIFT, KC.KB_P),
            trans()
        ])
        self.l_bracket = KeySwitch([
            kc(KC.L_BRACKET),
            mc(KC.L_GUI, KC.L_BRACKET),
            mc(KC.L_SHIFT, KC.L_BRACKET),
            kc(KC.UP)
        ])
        self.r_bracket = KeySwitch([
            kc(KC.R_BRACKET),
            mc(KC.L_GUI, KC.R_BRACKET),
            mc(KC.L_SHIFT, KC.R_BRACKET),
            kc(KC.PAGE_UP)
        ])
        self.back_slash = KeySwitch([
            kc(KC.BACK_SLASH),
            mc(KC.L_GUI, KC.BACK_SLASH),
            mc(KC.L_SHIFT, KC.BACK_SLASH),
            trans()
        ])

        self.caps = KeySwitch([
            la(Layer.FUNCS),
            trans(),
            trans(),
            trans()
        ])
        self.kb_a = KeySwitch([
            kc(KC.KB_A),
            mc(KC.L_GUI, KC.KB_A),
            mc(KC.L_SHIFT, KC.KB_A),
            kc(KC.HOME)
        ])
        self.kb_s = KeySwitch([
            kc(KC.KB_S),
            mc(KC.L_GUI, KC.KB_S),
            mc(KC.L_SHIFT, KC.KB_S),
            kc(KC.LEFT)
        ])
        self.kb_d = KeySwitch([
            kc(KC.KB_D),
            mc(KC.L_GUI, KC.KB_D),
            mc(KC.L_SHIFT, KC.KB_D),
            kc(KC.RIGHT)
        ])
        self.kb_f = KeySwitch([
            kc(KC.KB_F),
            mc(KC.L_GUI, KC.KB_F),
            mc(KC.L_SHIFT, KC.KB_F),
            kc(KC.END)
        ])
        self.kb_g = KeySwitch([
            kc(KC.KB_G),
            mc(KC.L_GUI, KC.KB_G),
            mc(KC.L_SHIFT, KC.KB_G),
            trans()
        ])
        self.kb_h = KeySwitch([
            kc(KC.KB_H),
            mc(KC.L_GUI, KC.KB_H),
            mc(KC.L_SHIFT, KC.KB_H),
            trans()
        ])
        self.kb_j = KeySwitch([
            kc(KC.KB_J),
            mc(KC.L_GUI, KC.KB_J),
            mc(KC.L_SHIFT, KC.KB_J),
            trans()
        ])
        self.kb_k = KeySwitch([
            kc(KC.KB_K),
            mc(KC.L_GUI, KC.KB_K),
            mc(KC.L_SHIFT, KC.KB_K),
            trans()
        ])
        self.kb_l = KeySwitch([
            kc(KC.KB_L),
            mc(KC.L_GUI, KC.KB_L),
            mc(KC.L_SHIFT, KC.KB_L),
            trans()
        ])
        self.semi_colon = KeySwitch([
            kc(KC.SEMI_COLON),
            mc(KC.L_GUI, KC.SEMI_COLON),
            mc(KC.L_SHIFT, KC.SEMI_COLON),
            kc(KC.LEFT)
        ])
        self.quote = KeySwitch([
            kc(KC.QUOTE),
            mc(KC.L_GUI, KC.QUOTE),
            mc(KC.L_SHIFT, KC.QUOTE),
            kc(KC.RIGHT)
        ])
        self.enter = KeySwitch([
            kc(KC.ENTER),
            mc(KC.L_GUI, KC.ENTER),
            mc(KC.L_SHIFT, KC.ENTER),
            trans()
        ])

        self.l_shift = KeySwitch([
            kc(KC.L_SHIFT),
            trans(),
            trans(),
            trans()
        ])
        self.kb_z = KeySwitch([
            kc(KC.KB_Z),
            mc(KC.L_GUI, KC.KB_Z),
            mc(KC.L_SHIFT, KC.KB_Z),
            trans()
        ])
        self.kb_x = KeySwitch([
            kc(KC.KB_X),
            mc(KC.L_GUI, KC.KB_X),
            mc(KC.L_SHIFT, KC.KB_X),
            kc(KC.DOWN)
        ])
        self.kb_c = KeySwitch([
            kc(KC.KB_C),
            mc(KC.L_GUI, KC.KB_C),
            mc(KC.L_SHIFT, KC.KB_C),
            kc(KC.PAGE_DOWN)
        ])
        self.kb_v = KeySwitch([
            kc(KC.KB_V),
            mc(KC.L_GUI, KC.KB_V),
            mc(KC.L_SHIFT, KC.KB_V),
            trans()
        ])
        self.kb_b = KeySwitch([
            kc(KC.KB_B),
            mc(KC.L_GUI, KC.KB_B),
            mc(KC.L_SHIFT, KC.KB_B),
            trans()
        ])
        self.kb_n = KeySwitch([
            kc(KC.KB_N),
            mc(KC.L_GUI, KC.KB_N),
            mc(KC.L_SHIFT, KC.KB_N),
            trans()
        ])
        self.kb_m = KeySwitch([
            kc(KC.KB_M),
            mc(KC.L_GUI, KC.KB_M),
            mc(KC.L_SHIFT, KC.KB_M),
            trans()
        ])
        self.comma = KeySwitch([
            kc(KC.COMMA),
            mc(KC.L_GUI, KC.COMMA),
            mc(KC.L_SHIFT, KC.COMMA),
            mc(KC.R_ALT, KC.LEFT)
        ])
        self.dot = KeySwitch([
            kc(KC.DOT),
            mc(KC.L_GUI, KC.DOT),
            mc(KC.L_SHIFT, KC.DOT),
            mc(KC.R_ALT, KC.RIGHT)
        ])
        self.slash = KeySwitch([
            kc(KC.SLASH),
            mc(KC.L_GUI, KC.SLASH),
            mc(KC.L_SHIFT, KC.SLASH),
            kc(KC.DOWN)
        ])
        self.r_shift = KeySwitch([
            kc(KC.R_SHIFT),
            trans(),
            trans(),
            trans()
        ])

        self.l_ctrl = KeySwitch([
            kc(KC.L_CTRL),
            trans(),
            trans(),
            trans()
        ])
        self.l_gui = KeySwitch([
            kc(KC.L_GUI),
            trans(),
            trans(),
            trans()
        ])
        self.l_alt = KeySwitch([
            kc(KC.L_ALT),
            trans(),
            trans(),
            trans()
        ])
        self.l_space = KeySwitch([
            lt(Layer.LOWER, KC.LANG_2),
            trans(),
            trans(),
            trans()
        ])
        self.space = KeySwitch([
            kc(KC.SPACE),
            mc(KC.L_GUI, KC.SPACE),
            mc(KC.L_SHIFT, KC.SPACE),
            trans()
        ])
        self.r_space = KeySwitch([
            lt(Layer.RAISE, KC.LANG_1),
            trans(),
            trans(),
            trans()
        ])
        self.r_alt = KeySwitch([
            kc(KC.R_ALT),
            trans(),
            trans(),
            trans()
        ])
        self.r_gui = KeySwitch([
            kc(KC.R_GUI),
            trans(),
            trans(),
            trans()
        ])
        self.r_ctrl = KeySwitch([
            kc(KC.R_CTRL),
            trans(),
            trans(),
            trans()
        ])
        self.func = KeySwitch([
            la(Layer.FUNCS),
            trans(),
            trans(),
            trans()
        ])

        self.l_space2 = KeySwitch([
            lt(Layer.LOWER, KC.LANG_2),
            trans(),
            trans(),
            trans()
        ])
        self.space2 = KeySwitch([
            kc(KC.SPACE),
            mc(KC.L_GUI, KC.SPACE),
            mc(KC.L_SHIFT, KC.SPACE),
            trans()
        ])
        self.r_space2 = KeySwitch([
            lt(Layer.RAISE, KC.LANG_1),
            trans(),
            trans(),
            trans()
        ])


class Column17ansi:
    """例としてColumn17のansi配列を実装している
    """

    def __init__(self):
        """キーボードの初期化
        キースイッチクラスタを生成し、I2CScannerを使うのでI/Oエクスパンダにそれを割り当ててて、
        とりあえず、ModelessProcessorで処理するようにしている
        """

        # スイッチとI/Oエクスパンダのリストを生成
        self.sw = Switches()
        self.expanders = []

        expander = TCA9555(0x00)
        expander.assign(0, self.sw.esc)
        expander.assign(1, self.sw.kb_1)
        expander.assign(2, self.sw.kb_2)
        expander.assign(3, self.sw.kb_3)
        expander.assign(4, self.sw.kb_4)
        expander.assign(5, self.sw.kb_5)
        expander.assign(8, self.sw.tab)
        expander.assign(9, self.sw.kb_q)
        expander.assign(10, self.sw.kb_w)
        expander.assign(11, self.sw.kb_e)
        expander.assign(12, self.sw.kb_r)
        expander.assign(13, self.sw.kb_t)
        self.expanders.append(expander)

        expander = TCA9555(0x01)
        expander.assign(0, self.sw.caps)
        expander.assign(1, self.sw.kb_a)
        expander.assign(2, self.sw.kb_s)
        expander.assign(3, self.sw.kb_d)
        expander.assign(4, self.sw.kb_f)
        expander.assign(5, self.sw.kb_g)
        expander.assign(8, self.sw.l_shift)
        expander.assign(9, self.sw.kb_z)
        expander.assign(10, self.sw.kb_x)
        expander.assign(11, self.sw.kb_c)
        expander.assign(12, self.sw.kb_v)
        expander.assign(13, self.sw.kb_b)
        self.expanders.append(expander)

        expander = TCA9555(0x02)
        expander.assign(0, self.sw.kb_6)
        expander.assign(1, self.sw.kb_7)
        expander.assign(2, self.sw.kb_8)
        expander.assign(3, self.sw.kb_9)
        expander.assign(4, self.sw.kb_0)
        expander.assign(5, self.sw.minus)
        expander.assign(6, self.sw.equal)
        expander.assign(7, self.sw.back_space)
        expander.assign(8, self.sw.kb_y)
        expander.assign(9, self.sw.kb_u)
        expander.assign(10, self.sw.kb_i)
        expander.assign(11, self.sw.kb_o)
        expander.assign(12, self.sw.kb_p)
        expander.assign(13, self.sw.l_bracket)
        expander.assign(14, self.sw.r_bracket)
        expander.assign(15, self.sw.back_slash)
        self.expanders.append(expander)

        expander = TCA9555(0x03)
        expander.assign(0, self.sw.kb_h)
        expander.assign(1, self.sw.kb_j)
        expander.assign(2, self.sw.kb_k)
        expander.assign(3, self.sw.kb_l)
        expander.assign(4, self.sw.semi_colon)
        expander.assign(5, self.sw.quote)
        expander.assign(6, self.sw.enter)
        expander.assign(8, self.sw.kb_n)
        expander.assign(9, self.sw.kb_m)
        expander.assign(10, self.sw.comma)
        expander.assign(11, self.sw.dot)
        expander.assign(12, self.sw.slash)
        expander.assign(13, self.sw.r_shift)
        self.expanders.append(expander)

        expander = TCA9555(0x04)
        expander.assign(0, self.sw.l_ctrl)
        expander.assign(1, self.sw.l_gui)
        expander.assign(2, self.sw.l_alt)
        expander.assign(3, self.sw.l_space)
        expander.assign(4, self.sw.space)
        expander.assign(5, self.sw.r_space)
        expander.assign(6, self.sw.func)
        expander.assign(7, self.sw.r_gui)
        expander.assign(8, self.sw.r_alt)
        expander.assign(9, self.sw.r_ctrl)
        expander.assign(10, self.sw.l_space2)
        expander.assign(11, self.sw.space2)
        expander.assign(12, self.sw.r_space2)
        self.expanders.append(expander)

        # I2Cマスタの生成
        i2c = I2C(GP5, GP4)
        while not i2c.try_lock():
            pass

        # プロセッサの生成
        kbd = WrappedKeyboard(Keyboard(usb_hid.devices))
        # kbd = Keyboard(usb_hid.devices)
        proc = LayeredProcessor(kbd)

        # スキャナの生成
        self.scanner = I2CScanner(self.expanders, i2c, proc)
