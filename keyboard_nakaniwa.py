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
from busio import I2C
from adafruit_hid.keyboard import Keyboard

from makbe.i2c_scanner import I2CScanner
from makbe.key_switch import KeySwitch
from makbe import kc, TCA9555, mc, mt, KeyCode, lt, trans
from makbe.layered_processor import LayeredProcessor
from makbe.sender import Sender


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
            trans(),
            trans()
        ])
        self.kb_1 = KeySwitch([
            kc(KC.KB_1),
            kc(KC.F1),
            trans(),
            trans()
        ])
        self.kb_2 = KeySwitch([
            kc(KC.KB_2),
            kc(KC.F2),
            trans(),
            trans()
        ])
        self.kb_3 = KeySwitch([
            kc(KC.KB_3),
            kc(KC.F3),
            trans(),
            trans()
        ])
        self.kb_4 = KeySwitch([
            kc(KC.KB_4),
            kc(KC.F4),
            trans(),
            trans()
        ])
        self.kb_5 = KeySwitch([
            kc(KC.KB_5),
            kc(KC.F5),
            trans(),
            trans()
        ])
        self.kb_6 = KeySwitch([
            kc(KC.KB_6),
            kc(KC.F6),
            trans(),
            trans()
        ])
        self.kb_7 = KeySwitch([
            kc(KC.KB_7),
            kc(KC.F7),
            trans(),
            trans()
        ])
        self.kb_8 = KeySwitch([
            kc(KC.KB_8),
            kc(KC.F8),
            trans(),
            trans()
        ])
        self.kb_9 = KeySwitch([
            kc(KC.KB_9),
            kc(KC.F9),
            trans(),
            trans()
        ])
        self.kb_0 = KeySwitch([
            kc(KC.KB_0),
            kc(KC.F10),
            trans(),
            trans()
        ])
        self.minus = KeySwitch([
            kc(KC.MINUS),
            kc(KC.F11),
            trans(),
            trans()
        ])
        self.equal = KeySwitch([
            kc(KC.EQUAL),
            kc(KC.F12),
            trans(),
            trans()
        ])
        self.back_slash = KeySwitch([
            kc(KC.BACK_SLASH),
            trans(),
            trans(),
            trans()
        ])
        self.grave = KeySwitch([
            kc(KC.GRAVE),
            trans(),
            trans(),
            trans()
        ])

        self.tab = KeySwitch([
            kc(KC.TAB),
            mc(KC.L_GUI, KC.TAB),
            trans(),
            trans()
        ])
        self.kb_q = KeySwitch([
            kc(KC.KB_Q),
            mc(KC.L_GUI, KC.KB_Q),
            trans(),
            trans()
        ])
        self.kb_w = KeySwitch([
            kc(KC.KB_W),
            mc(KC.L_GUI, KC.KB_W),
            trans(),
            trans()
        ])
        self.kb_e = KeySwitch([
            kc(KC.KB_E),
            mc(KC.L_GUI, KC.KB_E),
            trans(),
            trans()
        ])
        self.kb_r = KeySwitch([
            kc(KC.KB_R),
            mc(KC.L_GUI, KC.KB_R),
            trans(),
            trans()
        ])
        self.kb_t = KeySwitch([
            kc(KC.KB_T),
            mc(KC.L_GUI, KC.KB_T),
            trans(),
            trans()
        ])
        self.kb_y = KeySwitch([
            kc(KC.KB_Y),
            mc(KC.L_GUI, KC.KB_Y),
            trans(),
            trans()
        ])
        self.kb_u = KeySwitch([
            kc(KC.KB_U),
            mc(KC.L_GUI, KC.KB_U),
            trans(),
            trans()
        ])
        self.kb_i = KeySwitch([
            kc(KC.KB_I),
            mc(KC.L_GUI, KC.KB_I),
            trans(),
            kc(KC.F8)
        ])
        self.kb_o = KeySwitch([
            kc(KC.KB_O),
            mc(KC.L_GUI, KC.KB_O),
            trans(),
            kc(KC.F9)
        ])
        self.kb_p = KeySwitch([
            kc(KC.KB_P),
            mc(KC.L_GUI, KC.KB_P),
            trans(),
            kc(KC.F10)
        ])
        self.l_bracket = KeySwitch([
            kc(KC.L_BRACKET),
            mc(KC.L_GUI, KC.L_BRACKET),
            trans(),
            trans()
        ])
        self.r_bracket = KeySwitch([
            kc(KC.R_BRACKET),
            mc(KC.L_GUI, KC.R_BRACKET),
            trans(),
            trans()
        ])
        self.back_space = KeySwitch([
            kc(KC.BACK_SPACE),
            kc(KC.DELETE),
            trans(),
            trans()
        ])

        self.caps = KeySwitch([
            kc(KC.CAPS_LOCK),
            mc(KC.L_GUI, KC.CAPS_LOCK),
            trans(),
            trans()
        ])
        self.kb_a = KeySwitch([
            kc(KC.KB_A),
            mc(KC.L_GUI, KC.KB_A),
            trans(),
            trans()
        ])
        self.kb_s = KeySwitch([
            kc(KC.KB_S),
            mc(KC.L_GUI, KC.KB_S),
            trans(),
            trans()
        ])
        self.kb_d = KeySwitch([
            kc(KC.KB_D),
            mc(KC.L_GUI, KC.KB_D),
            trans(),
            trans()
        ])
        self.kb_f = KeySwitch([
            kc(KC.KB_F),
            mc(KC.L_GUI, KC.KB_F),
            trans(),
            trans()
        ])
        self.kb_g = KeySwitch([
            kc(KC.KB_G),
            mc(KC.L_GUI, KC.KB_G),
            trans(),
            trans()
        ])
        self.kb_h = KeySwitch([
            kc(KC.KB_H),
            mc(KC.L_GUI, KC.KB_H),
            trans(),
            trans()
        ])
        self.kb_j = KeySwitch([
            kc(KC.KB_J),
            mc(KC.L_GUI, KC.KB_J),
            trans(),
            trans()
        ])
        self.kb_k = KeySwitch([
            kc(KC.KB_K),
            mc(KC.L_GUI, KC.KB_K),
            trans(),
            trans()
        ])
        self.kb_l = KeySwitch([
            kc(KC.KB_L),
            mc(KC.L_GUI, KC.KB_L),
            trans(),
            trans()
        ])
        self.semi_colon = KeySwitch([
            kc(KC.SEMI_COLON),
            kc(KC.QUOTE),
            trans(),
            trans()
        ])
        self.quote = KeySwitch([
            kc(KC.QUOTE),
            mc(KC.L_GUI, KC.QUOTE),
            trans(),
            trans()
        ])
        self.enter = KeySwitch([
            kc(KC.ENTER),
            mc(KC.L_GUI, KC.ENTER),
            trans(),
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
            trans(),
            trans()
        ])
        self.kb_x = KeySwitch([
            kc(KC.KB_X),
            mc(KC.L_GUI, KC.KB_X),
            trans(),
            trans()
        ])
        self.kb_c = KeySwitch([
            kc(KC.KB_C),
            mc(KC.L_GUI, KC.KB_C),
            trans(),
            trans()
        ])
        self.kb_v = KeySwitch([
            kc(KC.KB_V),
            mc(KC.L_GUI, KC.KB_V),
            trans(),
            trans()
        ])
        self.kb_b = KeySwitch([
            kc(KC.KB_B),
            mc(KC.L_GUI, KC.KB_B),
            trans(),
            trans()
        ])
        self.kb_n = KeySwitch([
            kc(KC.KB_N),
            mc(KC.L_GUI, KC.KB_N),
            trans(),
            trans()
        ])
        self.kb_m = KeySwitch([
            kc(KC.KB_M),
            mc(KC.L_GUI, KC.KB_M),
            trans(),
            trans()
        ])
        self.comma = KeySwitch([
            kc(KC.COMMA),
            mc(KC.L_GUI, KC.COMMA),
            trans(),
            trans()
        ])
        self.dot = KeySwitch([
            kc(KC.DOT),
            mc(KC.L_GUI, KC.DOT),
            trans(),
            trans()
        ])
        self.slash = KeySwitch([
            kc(KC.SLASH),
            mc(KC.L_GUI, KC.SLASH),
            trans(),
            trans()
        ])
        self.r_shift = KeySwitch([
            kc(KC.R_SHIFT),
            trans(),
            trans(),
            trans()
        ])
        self.up = KeySwitch([
            kc(KC.UP),
            kc(KC.PAGE_UP),
            trans(),
            trans()
        ])
        self.delete = KeySwitch([
            kc(KC.DELETE),
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
            kc(KC.SPACE),
            trans(),
            trans(),
            trans()
        ])
        self.l_alt = KeySwitch([
            lt(Layer.LOWER, KC.L_GUI),
            trans(),
            trans(),
            trans()
        ])
        self.r_gui = KeySwitch([
            mt(KC.R_SHIFT, KC.R_GUI),
            trans(),
            trans(),
            trans()
        ])
        self.r_space = KeySwitch([
            kc(KC.SPACE),
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
        self.left = KeySwitch([
            kc(KC.LEFT),
            kc(KC.HOME),
            trans(),
            trans()
        ])
        self.down = KeySwitch([
            kc(KC.DOWN),
            kc(KC.PAGE_DOWN),
            trans(),
            trans()
        ])
        self.right = KeySwitch([
            kc(KC.RIGHT),
            kc(KC.END),
            trans(),
            trans()
        ])
        self.exp1 = KeySwitch([
            kc(KC.KB_6),
            trans(),
            trans(),
            trans()
        ])
        self.exp2 = KeySwitch([
            kc(KC.KB_B),
            trans(),
            trans(),
            trans()
        ])
        self.dmy1 = KeySwitch([
            kc(KC.KB_1),
            trans(),
            trans(),
            trans()
        ])
        self.dmy2 = KeySwitch([
            kc(KC.KB_2),
            trans(),
            trans(),
            trans()
        ])
        self.dmy3 = KeySwitch([
            kc(KC.KB_3),
            trans(),
            trans(),
            trans()
        ])
        self.dmy4 = KeySwitch([
            kc(KC.KB_4),
            trans(),
            trans(),
            trans()
        ])


class Nakaniwa:
    """例としてColumn13のansi配列を実装している
    """

    def __init__(self, scl, sda):
        """キーボードの初期化
        キースイッチクラスタを生成し、I2CScannerを使うのでI/Oエクスパンダにそれを割り当ててて、
        とりあえず、ModelessProcessorで処理するようにしている
        """

        # スイッチとI/Oエクスパンダのリストを生成
        self.sw = Switches()
        self.expanders = []
        self.scl = scl
        self.sda = sda

        # キーの割り当て、1つ目
        expander = TCA9555(0x00)
        expander.assign(0, self.sw.esc)
        expander.assign(1, self.sw.kb_1)
        expander.assign(2, self.sw.kb_2)
        expander.assign(3, self.sw.kb_3)
        expander.assign(4, self.sw.kb_4)
        expander.assign(5, self.sw.kb_5)
        expander.assign(6, self.sw.exp1)
        expander.assign(7, self.sw.tab)
        expander.assign(8, self.sw.kb_q)
        expander.assign(9, self.sw.kb_w)
        expander.assign(10, self.sw.kb_e)
        expander.assign(11, self.sw.kb_r)
        expander.assign(12, self.sw.kb_t)
        expander.assign(13, self.sw.caps)
        expander.assign(14, self.sw.kb_a)
        expander.assign(15, self.sw.kb_s)
        self.expanders.append(expander)

        # キーの割り当て、2つ目
        expander = TCA9555(0x01)
        expander.assign(0, self.sw.kb_d)
        expander.assign(1, self.sw.kb_f)
        expander.assign(2, self.sw.kb_g)
        expander.assign(3, self.sw.l_shift)
        expander.assign(4, self.sw.kb_z)
        expander.assign(5, self.sw.kb_x)
        expander.assign(6, self.sw.kb_c)
        expander.assign(7, self.sw.kb_v)
        expander.assign(8, self.sw.kb_b)
        expander.assign(9, self.sw.l_ctrl)
        expander.assign(10, self.sw.r_alt)
        expander.assign(11, self.sw.l_gui)
        expander.assign(12, self.sw.l_space)
        expander.assign(13, self.sw.l_alt)
        self.expanders.append(expander)

        # キーの割り当て、3つ目
        expander = TCA9555(0x02)
        expander.assign(0, self.sw.kb_6)
        expander.assign(1, self.sw.kb_7)
        expander.assign(2, self.sw.kb_8)
        expander.assign(3, self.sw.kb_9)
        expander.assign(4, self.sw.kb_0)
        expander.assign(5, self.sw.minus)
        expander.assign(6, self.sw.equal)
        expander.assign(7, self.sw.back_slash)
        expander.assign(8, self.sw.grave)
        expander.assign(9, self.sw.kb_y)
        expander.assign(10, self.sw.kb_u)
        expander.assign(11, self.sw.kb_i)
        expander.assign(12, self.sw.kb_o)
        expander.assign(13, self.sw.kb_p)
        expander.assign(14, self.sw.l_bracket)
        expander.assign(15, self.sw.r_bracket)
        self.expanders.append(expander)

        # キーの割り当て、4つ目
        expander = TCA9555(0x03)
        expander.assign(0, self.sw.back_space)
        expander.assign(1, self.sw.kb_h)
        expander.assign(2, self.sw.kb_j)
        expander.assign(3, self.sw.kb_k)
        expander.assign(4, self.sw.kb_l)
        expander.assign(5, self.sw.semi_colon)
        expander.assign(6, self.sw.quote)
        expander.assign(7, self.sw.enter)
        expander.assign(8, self.sw.exp2)
        expander.assign(9, self.sw.kb_n)
        expander.assign(10, self.sw.kb_m)
        expander.assign(11, self.sw.comma)
        expander.assign(12, self.sw.dot)
        expander.assign(13, self.sw.slash)
        expander.assign(14, self.sw.r_shift)
        expander.assign(15, self.sw.up)
        self.expanders.append(expander)

        # キーの割り当て、5つ目
        expander = TCA9555(0x04)
        expander.assign(0, self.sw.delete)
        expander.assign(1, self.sw.r_gui)
        expander.assign(2, self.sw.dmy1)
        expander.assign(3, self.sw.r_space)
        expander.assign(4, self.sw.dmy3)
        expander.assign(5, self.sw.r_gui)
        expander.assign(6, self.sw.left)
        expander.assign(7, self.sw.down)
        expander.assign(8, self.sw.right)
        self.expanders.append(expander)

        # I2Cマスタの生成
        i2c = I2C(self.scl, self.sda)
        while not i2c.try_lock():
            pass

        print([hex(addr) for addr in i2c.scan()])

        # プロセッサの生成
        kbd = Keyboard(usb_hid.devices)
        proc = LayeredProcessor(Sender(kbd))

        # スキャナの生成
        self.scanner = I2CScanner(self.expanders, i2c, proc)
