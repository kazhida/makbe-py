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

from makbe.key_code import KeyCode


class Action:

    def layer(self):
        return None

    def key_codes(self):
        return []


class NoOp(Action):

    def __init__(self):
        super(NoOp, self).__init__(self)


class Trans(Action):

    def __init__(self):
        super(Trans, self).__init__(self)


class SingleKeyCode(Action):

    def __init__(self, code: KeyCode):
        self.code = code

    def key_codes(self):
        return [self.code]


class MultipleKeyCodes(Action):

    def __init__(self, codes: [KeyCode]):
        self.codes = codes

    def key_codes(self):
        return self.codes


class Layer(Action):

    def __init__(self, layer: int):
        self.layer = layer

    def layer(self):
        return self.layer


class DefaultLayer(Action):

    def __init__(self, layer: int):
        self.layer = layer

    def layer(self):
        return self.layer


class HoldTap(Action):
    def __init__(self, hold: Action, tap: Action, timeout: int = 200):
        self.hold = hold
        self.tap = tap
        self.timeout = timeout


def k(kc: KeyCode) -> Action:
    return SingleKeyCode(kc)


def la(layer: int) -> Action:
    return Layer(layer)


def d(layer: int) -> Action:
    return DefaultLayer(layer)


def m(kcs: [KeyCode]) -> Action:
    return MultipleKeyCodes(kcs)


def lt(layer:int, kc: KeyCode) -> Action:
    return HoldTap(la(layer), SingleKeyCode(kc))


def mt(modifier: KeyCode, kc: KeyCode) -> Action:
    return HoldTap(SingleKeyCode(modifier), SingleKeyCode(kc))
