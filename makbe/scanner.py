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
from time import monotonic_ns


class Scanner():
    """キースキャンをするクラス
    このクラスを継承したクラスで、スキャン時の動作を定義する
    """

    def __init__(self, event_queue, processor):
        self.event_queue = event_queue
        self.processor = processor

    def scan(self):
        """
        スキャンする
        """
        pass

    def process_events(self):
        """
        キューに溜まったイベントをプロセッサで処理する
        """
        now = monotonic_ns() // 1000 // 1000

        # キューから全てのイベントを処理
        while not self.event_queue.is_empty():
            item = self.event_queue.dequeue()
            if item is not None:
                event, timestamp = item
                self.processor.put(event, timestamp)

        # 最後にtickを呼び出す
        self.processor.tick(now)

    def update(self):
        """
        スキャンとイベント処理を両方実行（統合モード）
        """
        self.scan()
        self.process_events()
