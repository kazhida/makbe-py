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
from makbe import KeySwitch, Action, KeyEvent
from makbe.key_code import KeyCode
from makbe.reporter import Reporter


class KeyState:

    def __init__(self, switch):
        self.switch = switch

    def key_code(self):
        return None

    def get_layer(self):
        return None

    def release(self, switch):
        return self.switch == switch


class NormalKey(KeyState):

    def __init__(self, keycode: KeyCode, switch: KeySwitch):
        super().__init__(switch)
        self.keycode = keycode

    def key_code(self):
        return self.keycode


class LayerModifier(KeyState):

    def __init__(self, layer: int, switch: KeySwitch):
        super().__init__(switch)
        self.layer = layer

    def get_layer(self):
        return self.layer


class WaitingState:

    def __init__(self, switch: KeySwitch, timeout: int, hold: Action, tap: Action):
        self.switch = switch
        self.timeout = timeout
        self.hold = hold
        self.tap = tap

    def tick(self):
        self.timeout -= 1
        return self.timeout <= 0

    def is_corresponding_release(self, event: KeyEvent):
        return event.is_released() and event.switch == self.switch


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

    def push(self, event: EventSince):
        result = None
        position = self.tail % self.size
        if self.tail >= self.size:
            result = self.buffer[position]
        self.buffer[position] = event
        self.tail += 1
        self.tail %= self.size * 2
        return result


class Evaluator:

    def __init__(self):
        self.states: [KeyState] = []
        self.waiting: [WaitingState] = []
        self.stacked: [EventSince] = []

    def eval(self, event: KeyEvent, reporter: Reporter):
        pass

    def tick(self, reporter: Reporter):
        pass

    def waiting_into_hold(self):
        pass

    def waiting_into_tap(self):
        pass

    def unstack(self, stacked: EventSince):
        pass

    def keycodes(self):
        pass
