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

from board import A3, A2, A1, A0, SCK, MISO, MOSI, D4, D5, D6, D7

from adafruit_hid.keyboard import Keyboard

from makbe.key_switch import KeySwitch, nop_switch
from makbe import kc, TCA9555, mc, mt, KeyCode, lt, trans
from makbe.layered_processor import LayeredProcessor
from makbe.matrix_scanner import MatrixScanner
from makbe.sender import Sender
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
            lt(Layer.FUNCS, KC.ESCAPE),
            kc(KC.GRAVE),
            mc(KC.L_SHIFT, KC.GRAVE),
            trans()
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
            mc(KC.L_GUI, KC.TAB),
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
            mc(KC.L_GUI, KC.SEMI_COLON),
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
            mc(KC.R_SHIFT, KC.L_BRACKET),
            trans()
        ])
        self.dot = KeySwitch([
            kc(KC.DOT),
            kc(KC.R_BRACKET),
            mc(KC.R_SHIFT, KC.R_BRACKET),
            trans()
        ])
        self.up = KeySwitch([
            kc(KC.UP),
            kc(KC.PAGE_UP),
            mc(KC.L_GUI, KC.UP),
            trans()
        ])
        self.slash = KeySwitch([
            kc(KC.SLASH),
            kc(KC.BACK_SLASH),
            kc(KC.BACK_SLASH),
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
        self.delete = KeySwitch([
            kc(KC.DELETE),
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
            lt(Layer.LOWER, KC.LANG_2),
            trans(),
            trans(),
            trans()
        ])
        self.r_gui = KeySwitch([
            mt(KC.R_SHIFT, KC.LANG_1),
            trans(),
            trans(),
            trans()
        ])
        self.r_space = KeySwitch([
            lt(Layer.RAISE, KC.SPACE),
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
            mc(KC.L_GUI, KC.LEFT),
            trans()
        ])
        self.down = KeySwitch([
            kc(KC.DOWN),
            kc(KC.PAGE_DOWN),
            mc(KC.L_GUI, KC.DOWN),
            trans()
        ])
        self.right = KeySwitch([
            kc(KC.RIGHT),
            kc(KC.END),
            mc(KC.L_GUI, KC.RIGHT),
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

class HelixPicoRight:
    """例としてColumn13のansi配列を実装している
    """

    def __init__(self):
        """キーボードの初期化
        キースイッチクラスタを生成し、I2CScannerを使うのでI/Oエクスパンダにそれを割り当ててて、
        とりあえず、ModelessProcessorで処理するようにしている
        """
        # スイッチとI/Oエクスパンダのリストを生成

        cols = [A3, A2, A1, A0, SCK, MISO, MOSI]
        rows = [D4, D5, D6, D7]

        self.sw = Switches()
        self.matrix: list[list[KeySwitch]] = [
            [
                self.sw.kb_y,
                self.sw.kb_q,
                self.sw.kb_w,
                self.sw.kb_e,
                self.sw.kb_r,
                self.sw.kb_t,
                self.sw.slash
            ],
            [
                self.sw.kb_u,
                self.sw.kb_a,
                self.sw.kb_s,
                self.sw.kb_d,
                self.sw.kb_f,
                self.sw.kb_g,
                self.sw.minus
            ],
            [
                self.sw.kb_i,
                self.sw.kb_z,
                self.sw.kb_x,
                self.sw.kb_c,
                self.sw.kb_v,
                self.sw.kb_b,
                self.sw.semi_colon
            ],
            [
                self.sw.kb_o,
                self.sw.kb_h,
                self.sw.kb_j,
                self.sw.kb_k,
                self.sw.kb_l,
                self.sw.kb_n,
                self.sw.kb_m
            ]
        ]

        # プロセッサの生成
        kbd = WrappedKeyboard(Keyboard(usb_hid.devices))
        # kbd = Keyboard(usb_hid.devices)
        proc = LayeredProcessor(Sender(kbd))

        # スキャナの生成
        self.scanner = MatrixScanner(
            row2col = False,
            matrix = self.matrix,
            row_pins = rows,
            col_pins = cols,
            processor = proc,
            active_low = True,
            debug = True,
            drive_inactive = False)
