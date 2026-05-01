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
from adafruit_hid.keyboard import Keyboard
from board import SCL, SDA
from busio import I2C
from makbe import KeyCode, KeySwitch, kc, mc, trans, lt, I2CScanner
from makbe.expanders.pca9536 import PCA9536
from makbe.layered_processor import LayeredProcessor
from makbe.sender import Sender
from makbe.wrapped_kbd import WrappedKeyboard


class KC(KeyCode):      # KeyCodeが頻出するので短縮形を作っておく
    pass


class Layer:
    QWERTY = 0
    FUNCS = 1


class Switches:
    """キースイッチ一覧
    このライブラリでは、Switchesクラスとして使用するキースイッチを全部列挙する
    """

    def __init__(self):

        self.kb_h = KeySwitch([
            lt(Layer.FUNCS, KC.KB_H),
            trans()
        ])
        self.kb_j = KeySwitch([
            kc(KC.KB_J),
            mc(KC.L_GUI, KC.KB_X)
        ])
        self.kb_k = KeySwitch([
            kc(KC.KB_K),
            mc(KC.L_GUI, KC.KB_C)
        ])
        self.kb_l = KeySwitch([
            kc(KC.KB_L),
            mc(KC.L_GUI, KC.KB_V)
        ])

class CardPendant:
    """例としてColumn7のansi配列を実装している
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
        expander = PCA9536()
        expander.assign(0, self.sw.kb_h)
        expander.assign(1, self.sw.kb_j)
        expander.assign(2, self.sw.kb_k)
        expander.assign(3, self.sw.kb_l)

        self.expanders.append(expander)

        # I2Cマスタの生成
        i2c = I2C(SCL, SDA)
        while not i2c.try_lock():
            pass

        # プロセッサの生成
        kbd = WrappedKeyboard(Keyboard(usb_hid.devices))
        # kbd = Keyboard(usb_hid.devices)
        proc = LayeredProcessor(Sender(kbd))

        # スキャナの生成
        self.scanner = I2CScanner(self.expanders, i2c, proc)
