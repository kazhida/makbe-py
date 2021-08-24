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

class KeyEvent(object):
    """キーイベントの基底クラス
    KeyPressedとKeyReleasedがこれを継承している
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        self.switch = switch

    def is_pressed(self) -> bool:
        """
        :return: KeyPressedイベントならTrueを返す
        """
        return False

    def is_released(self) -> bool:
        """
        :return: KeyReleasedイベントならTrueを返す
        """
        return False


class KeyPressed(KeyEvent):
    """キーが押されたときのイベント
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        super().__init__(switch)

    def is_pressed(self) -> bool:
        """
        :return: Trueを返す
        """
        return True


class KeyReleased(KeyEvent):
    """キーが話されたときのイベント
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        super().__init__(switch)

    def is_released(self) -> bool:
        """
        :return: Trueを返す
        """
        return True


class EventSince:
    """キーイベントとそこからの経過時間（スキャン回数）の組み合わせ
    """

    def __init__(self, event: KeyEvent):
        """
        :param event: キーイベント
        """
        self.event = event
        self.since = 0

    def tick(self):
        """経過時間のインクリメント
        """
        self.since += 1


class EventQueue:
    """サイズ固定のリングバッファ
    イベントと経過時間を一定数保持するバッファ
    """

    def __init__(self, size: int):
        """
        :param size: バッファサイズ
        """
        self.buffer = []
        self.size = size
        self.tail = 0
        self.head = 0

    def push(self, event: KeyEvent):
        """イベントの追加
        :param event: キーイベント
        :return: サイズからあふれたらそれを返す、そうでなければNoneを返す
        """
        head_at = self.head % self.size
        tail_at = self.tail % self.size
        if self.tail < self.size:
            result = None
        else:
            result = self.buffer[head_at]
            self.head += 1
        self.buffer[tail_at] = EventSince(event)
        self.tail += 1
        return result

    def pop(self):
        """
        :return: バッファの先頭を取り出す
        """
        if self.tail == 0:
            return None
        elif self.head < self.tail:
            result = self.buffer[self.head % self.size]
            self.head += 1
            return result
        else:
            return None

    def count(self) -> int:
        """
        :return: バッファ無いのイベント数を返す
        """
        return min(self.tail, self.size)

    def get(self, index: int):
        """
        :param index: 位置（0オリジン）
        :return: EventSince 指定位置のイベント（経過時間付き）
        """
        if self.tail == 0:
            return None
        elif self.head < self.tail:
            index += self.head
            index %= self.size
            return self.buffer[index]
        else:
            return None


class EventIterator(object):
    """EventQueueのイテレータ
    """

    def __init__(self, queue: EventQueue):
        """
        :param queue:  EventQueue
        """
        self.queue = queue
        self.index = 0

    def __iter__(self):
        # __next__()はselfが実装してるのでそのままselfを返す
        return self

    def __next__(self):  # Python2だと next(self) で定義
        if self.index < self.queue.count():
            result = self.queue.get(self.index)
            self.index += 1
            return result
        else:
            raise StopIteration()
