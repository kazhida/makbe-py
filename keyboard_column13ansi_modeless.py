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
from board import SCL, SDA
from busio import I2C
from adafruit_hid.keyboard import Keyboard

from makbe.i2c_scanner import I2CScanner
from makbe.key_switch import KeySwitch
from makbe import kc, KeyCode, TCA9555
from makbe.layered_processor import LayeredProcessor


class Switches:
    """キースイッチ一覧
    このライブラリでは、Switchesクラスとして使用するキースイッチを全部列挙する
    """

    def __init__(self):
        self.esc = KeySwitch([kc(KeyCode.ESCAPE)])
        self.kb_q = KeySwitch([kc(KeyCode.KB_Q)])
        self.kb_w = KeySwitch([kc(KeyCode.KB_W)])
        self.kb_e = KeySwitch([kc(KeyCode.KB_E)])
        self.kb_r = KeySwitch([kc(KeyCode.KB_R)])
        self.kb_t = KeySwitch([kc(KeyCode.KB_T)])
        self.kb_y = KeySwitch([kc(KeyCode.KB_Y)])
        self.kb_u = KeySwitch([kc(KeyCode.KB_U)])
        self.kb_i = KeySwitch([kc(KeyCode.KB_I)])
        self.kb_o = KeySwitch([kc(KeyCode.KB_O)])
        self.kb_p = KeySwitch([kc(KeyCode.KB_P)])
        self.minus = KeySwitch([kc(KeyCode.MINUS)])
        self.back_space = KeySwitch([kc(KeyCode.BACK_SPACE)])

        self.tab = KeySwitch([kc(KeyCode.TAB)])
        self.kb_a = KeySwitch([kc(KeyCode.KB_A)])
        self.kb_s = KeySwitch([kc(KeyCode.KB_S)])
        self.kb_d = KeySwitch([kc(KeyCode.KB_D)])
        self.kb_f = KeySwitch([kc(KeyCode.KB_F)])
        self.kb_g = KeySwitch([kc(KeyCode.KB_G)])
        self.kb_h = KeySwitch([kc(KeyCode.KB_H)])
        self.kb_j = KeySwitch([kc(KeyCode.KB_J)])
        self.kb_k = KeySwitch([kc(KeyCode.KB_K)])
        self.kb_l = KeySwitch([kc(KeyCode.KB_L)])
        self.semi_colon = KeySwitch([kc(KeyCode.SEMI_COLON)])
        self.enter = KeySwitch([kc(KeyCode.ENTER)])

        self.l_shift = KeySwitch([kc(KeyCode.L_SHIFT)])
        self.kb_z = KeySwitch([kc(KeyCode.KB_Z)])
        self.kb_x = KeySwitch([kc(KeyCode.KB_X)])
        self.kb_c = KeySwitch([kc(KeyCode.KB_C)])
        self.kb_v = KeySwitch([kc(KeyCode.KB_V)])
        self.kb_b = KeySwitch([kc(KeyCode.KB_B)])
        self.kb_n = KeySwitch([kc(KeyCode.KB_N)])
        self.kb_m = KeySwitch([kc(KeyCode.KB_M)])
        self.comma = KeySwitch([kc(KeyCode.COMMA)])
        self.dot = KeySwitch([kc(KeyCode.DOT)])
        self.up = KeySwitch([kc(KeyCode.UP)])
        self.slash = KeySwitch([kc(KeyCode.SLASH)])

        self.l_ctrl = KeySwitch([kc(KeyCode.L_CTRL)])
        self.l_gui = KeySwitch([kc(KeyCode.L_GUI)])
        self.delete = KeySwitch([kc(KeyCode.DELETE)])
        self.l_alt = KeySwitch([kc(KeyCode.L_ALT)])
        self.l_space = KeySwitch([kc(KeyCode.SPACE)])
        self.r_space = KeySwitch([kc(KeyCode.SPACE)])
        self.r_gui = KeySwitch([kc(KeyCode.R_GUI)])
        self.r_alt = KeySwitch([kc(KeyCode.R_ALT)])
        self.left = KeySwitch([kc(KeyCode.LEFT)])
        self.down = KeySwitch([kc(KeyCode.DOWN)])
        self.right = KeySwitch([kc(KeyCode.RIGHT)])


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
        proc = LayeredProcessor(kbd)

        # スキャナの生成
        self.scanner = I2CScanner(self.expanders, i2c, proc)
