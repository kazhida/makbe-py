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


class EventQueue:
    """スキャナとプロセッサ間でイベントを受け渡すためのキュー
    """

    def __init__(self, max_size: int = 32):
        """
        :param max_size: キューの最大サイズ
        """
        self.queue = []
        self.max_size = max_size

    def enqueue(self, event: KeyEvent, timestamp: int):
        """イベントをキューに追加
        :param event: キーイベント
        :param timestamp: タイムスタンプ
        """
        if len(self.queue) < self.max_size:
            self.queue.append((event, timestamp))
        else:
            # キューがいっぱいの場合は古いイベントを削除
            print("Warning: Event queue full, dropping oldest event")
            self.queue.pop(0)
            self.queue.append((event, timestamp))

    def dequeue(self):
        """キューからイベントを取り出す
        :return: (event, timestamp) のタプル、またはキューが空の場合はNone
        """
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def is_empty(self) -> bool:
        """キューが空かどうか
        :return: 空の場合True
        """
        return len(self.queue) == 0

    def size(self) -> int:
        """キューに入っているイベント数
        :return: イベント数
        """
        return len(self.queue)