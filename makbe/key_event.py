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

from .key_switch import KeySwitch


class KeyEvent(object):

    def __init__(self, switch: KeySwitch):
        self.switch = switch

    def is_pressed(self) -> bool:
        return False

    def is_released(self) -> bool:
        return False


class KeyPressed(KeyEvent):

    def __init__(self, switch: KeySwitch):
        super().__init__(switch)

    def is_pressed(self) -> bool:
        return True


class KeyReleased(KeyEvent):

    def __init__(self, switch: KeySwitch):
        super().__init__(switch)

    def is_released(self) -> bool:
        return True


class EventSince:

    def __init__(self, event: KeyEvent):
        self.event = event
        self.since = 0

    def tick(self):
        self.since += 1


class EventQueue:

    def __init__(self, size: int):
        self.buffer = []
        self.size = size
        self.tail = 0
        self.head = 0

    def push(self, event: EventSince):
        head_at = self.head % self.size
        tail_at = self.tail % self.size
        if self.tail < self.size:
            result = None
        else:
            result = self.buffer[head_at]
            self.head += 1
        self.buffer[tail_at] = event
        self.tail += 1
        return result

    def pop(self):
        if self.tail == 0:
            return None
        elif self.head < self.tail:
            result = self.buffer[self.head % self.size]
            self.head += 1
            return result
        else:
            return None

    def count(self) -> int:
        return min(self.tail, self.size)

    def get(self, index: int):
        if self.tail == 0:
            return None
        elif self.head < self.tail:
            index += self.head
            index %= self.size
            return self.buffer[index]
        else:
            return None


class EventIterator(object):

    def __init__(self, queue: EventQueue):
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
