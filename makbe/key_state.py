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

from .key_code import KeyCode
from .key_switch import KeySwitch


class KeyState:

    def __init__(self, switch):
        self.switch = switch

    def key_code(self):
        return None

    def get_layer(self):
        return None

    def release(self, switch):
        if self.switch == switch:
            return self
        else:
            return None

    def tick(self) -> bool:
        return False


class NormalKeyState(KeyState):

    def __init__(self, keycode: KeyCode, switch: KeySwitch):
        super().__init__(switch)
        self.keycode = keycode

    def key_code(self):
        return self.keycode

    def tick(self) -> bool:
        return True


class LayerModifierState(KeyState):

    def __init__(self, layer: int, switch: KeySwitch):
        super().__init__(switch)
        self.layer = layer

    def get_layer(self):
        return self.layer

    def tick(self) -> bool:
        return True
