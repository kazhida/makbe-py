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

from enum import Enum, auto
from .action import Action, Trans
from .keyevent import KeyEvent, KeyPressed, KeyReleased


class Shape(Enum):
    Rectangle = auto()
    IsoEnter = auto()


class Rotation:

    def __init__(self, angle: float = 0, center_x: float = 0, center_y: float = 0):
        self.a = angle
        self.x = center_x
        self.y = center_y


class Position:

    def __init__(self, x: float = 0, y: float = 0, w: float = 1, h: float = 1, r: Rotation = Rotation()):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r


class Debouncer:

    def __init__(self, limit: int):
        self.current = False
        self.pressed = False
        self.count = 0
        self.limit = limit

    def update(self, pressed: bool) -> bool:
        if self.current == pressed:
            self.count = 0
            return False
        else:
            if self.pressed == pressed:
                self.count += 1
            else:
                self.pressed = pressed
                self.count = 1
            if self.count > self.limit:
                self.current = self.pressed
                self.count = 0
                return True
            else:
                return False


class KeySwitch:

    def __init__(self, position: Position, actions: [Action],
                 default: Action = Trans(),
                 shape: Shape = Shape.Rectangle,
                 debounce: int = 5):
        self.shape = shape
        self.position = position
        self.actions = actions
        self.default_action = default
        self.debouncer = Debouncer(debounce)

    def update(self, pressed: bool) -> KeyEvent:
        if not self.debouncer.update(pressed):
            return KeyEvent(self)
        elif self.debouncer.current:
            return KeyPressed(self)
        else:
            return KeyReleased(self)

    def action(self, layer: int) -> Action:
        if layer < len(self.actions):
            return self.actions[layer]
        else:
            return self.default_action


def dummy_switch() -> KeySwitch:
    return KeySwitch(Position(), [])
