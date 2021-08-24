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
from .key_event import KeyPressed, KeyReleased
from .io_expander import IoExpander
from .processor import Processor
from .scanner import Scanner


class I2CScanner(Scanner):
    """I2Cを使用したスキャナ
    moduloアーキテクチャに基づいたスキャナ
    """

    def __init__(self, expanders: [IoExpander], i2c, processor: Processor):
        """
        :param expanders: I/Oエクスパンダのリスト
        :param i2c: I2Cマスタ
        :param processor: キーイベントを処理するオブジェクト
        """
        self.processor = processor
        self.expanders = expanders
        self.i2c = i2c
        for d in expanders:
            d.init_device(i2c)

    def scan(self):
        """
        I/Oエクスパンダをスキャンして、プロセッサに渡す
        """
        for d in self.expanders:
            for i, p in enumerate(d.read_device(self.i2c)):
                switch = d.switch(i)
                event = switch.update(p)
                self.processor.put(event)
