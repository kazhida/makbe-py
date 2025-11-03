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
from makbe import KeyEvent


class Processor:
    """プロセッサの基底クラス
    """

    def put(self, event: KeyEvent, now: int):
        """
        :param event: 処理するイベント
        :param now: 現在時刻に相当する数値（ms単位）
        """
        pass

    def tick(self, now: int):
        """
        一通りのイベントをput()で渡した後に、定期的に呼び出すメソッド
        :param now: 現在時刻に相当する数値（ms単位）
        """
        pass

    def process_queue(self, event_queue, now: int):
        """
        キューからイベントを取り出して処理する
        :param event_queue: EventQueueオブジェクト
        :param now: 現在時刻に相当する数値（ms単位）
        """
        # キューから全てのイベントを処理
        while not event_queue.is_empty():
            item = event_queue.dequeue()
            if item is not None:
                event, timestamp = item
                self.put(event, timestamp)

        # 最後にtickを呼び出す
        self.tick(now)