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
from makbe import KeyEvent, KeyPressed, KeyReleased
from makbe.processor import Processor


class ModelessProcessor(Processor):
    """デバウンス以外の内部処理をしないプロセッサ
    レイヤやHoldTapを使用しない場合は、このプロセッサで十分
    このライブラリの内部処理のバグから逃れられる
    """

    def __init__(self, kbd):
        """
        :param kbd: CircuitPythonのadafruit_hid.keyboard.Keyboard
        """
        self.kbd = kbd

    def put(self, event: KeyEvent, now: int):
        """イベントの処理
        イベントをそのままKeyboardに渡す
        :param event: 処理するイベント
        :param now: 現在時刻に相当する数値（ns単位）
        """
        if isinstance(event, KeyPressed):
            print(str(event))
            self.kbd.press(event.switch.action(0).key_code)
        if isinstance(event, KeyReleased):
            print(str(event))
            self.kbd.release(event.switch.action(0).key_code)

    def tick(self, now: int):
        pass
