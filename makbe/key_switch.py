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
from makbe.action import Action


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


class KeyEvent(Enum):
    Pressed = auto()
    Released = auto()


# class KeyState:


class KeySwitch:

    def __init__(self, position: Position, actions: [Action], shape: Shape = Shape.Rectangle):
        self.shape = shape
        self.position = position
        self.actions = actions
