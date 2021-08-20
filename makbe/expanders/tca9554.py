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
from .. import nop_switch, IoExpander, KeySwitch


class TCA9554(IoExpander):
    """TCA9554（PCA9554も同じ）
    """

    def __init__(self, dev_address: int):
        """デバイスアドレスを指定してオブジェクトを生成
        上位4ビット分は固定なので、下位3ビット部分だけを指定する
        :param dev_address: デバイスアドレスの下位3ビット分
        """
        self.dev_address = dev_address + 0x20
        self.switches = []
        for i in range(8):
            self.switches.append(nop_switch())

    def init_device(self, i2c) -> bool:
        """I2Cの初期化
        :param i2c: I2Cマスタ
        :return: Trueを返す
        """
        i2c.writeto(self.dev_address, bytes([0x03, 0xFF]), True)
        return True

    def read_device(self, i2c) -> [bool]:
        """I/Oエクスパンダを読み込んで、その状態を返す
        :param i2c: I2Cマスタ
        :return: 各ピンの状態（ONでTrue）のリストを返す
        """
        i2c.writeto(self.dev_address, bytes([0x00]), False)
        buffer = bytearray(1)
        i2c.readfrom_into(self.dev_address, buffer)
        result = []
        for p in range(8):
            mask = 1 << p
            if buffer[0] & mask != 0:
                result.append(True)
            else:
                result.append(False)
        return result

    def assign(self, pin: int, switch: KeySwitch):
        """ピンにキースイッチを割り当てる
        :param pin: ピン番号（0オリジン）
        :param switch: キースイッチ
        """
        self.switches[pin] = switch

    def switch(self, pin: int) -> KeySwitch:
        """ピンに対応するキースイッチを返す
        :param pin: ピン番号（0オリジン）
        :return: 対応するキースイッチ
        """
        return self.switches[pin]
