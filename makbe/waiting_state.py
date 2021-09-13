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

from .action import Action, NoOp
from .key_event import KeyEvent
from .key_switch import KeySwitch, EMPTY_SWITCH


class WaitingState:
    """HoldTapを処理するためのなにか
    Keyberonからのベタ移植なので、仕組みはまだ分かっていない(^^;
    """

    def __init__(self, switch: KeySwitch, timeout: int, hold: Action, tap: Action):
        self.switch = switch
        self.timeout = timeout
        self.hold = hold
        self.tap = tap

    def is_empty(self) -> bool:
        return self.switch is EMPTY_SWITCH

    def is_not_empty(self) -> bool:
        return not self.is_empty()

    def tick(self) -> bool:
        self.timeout -= 1
        return self.timeout <= 0

    def is_corresponding_release(self, event: KeyEvent):
        return event.is_released() and event.switch == self.switch and self.switch is not EMPTY_SWITCH

    def do_tap(self, do_action):
        if self.is_not_empty():
            tap = self.tap
            switch = self.switch
            self.switch = EMPTY_SWITCH
            do_action(tap, switch, 0)

    def do_hold(self, do_action):
        if self.is_not_empty():
            hold = self.hold
            switch = self.switch
            self.switch = EMPTY_SWITCH
            do_action(hold, switch, 0)

    @staticmethod
    def empty():
        return WaitingState(EMPTY_SWITCH, 0, NoOp(), NoOp())
