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
from . import KeySwitch
from .key_event import KeyEvent, KeyReleased, KeyPressed
from .processor import Processor
from .actions import *


class WaitingState:

    def __init__(self, action: Action, switch: KeySwitch, pressed_at: int):
        self.action = action
        self.pressed_at = pressed_at
        self.switch = switch

    def held(self, now: int) -> bool:
        action = self.action
        if isinstance(action, HoldTapAction):
            return self.pressed_at > 0 and now > self.pressed_at + action.timeout
        return False


class LayeredProcessor(Processor):

    def __init__(self, kbd):
        self.layer = 0
        self.waitingStates: [WaitingState] = []
        self.kbd = kbd

    def put(self, event: KeyEvent, now: int):
        """
        :param event: 処理するイベント
        :param now: 現在時刻に相当する数値（ns単位）
        """
        # レイヤを決める
        for state in self.waitingStates:
            action = state.action
            self.set_layer(action, state.held(now))
        print("layer: %d" % self.layer)
        # 押されたとき
        if isinstance(event, KeyPressed):
            print("on_pressed")
            switch = event.switch
            action = switch.actions[self.layer]
            if isinstance(action, TransAction):
                action = self.find_action(switch, self.layer)
            if isinstance(action, SingleKeyCode):
                self.kbd.press(action.key_code)
            if isinstance(action, MultipleKeyCodes):
                for code in action.key_codes:
                    self.kbd.press(code)
            state = WaitingState(action, switch, now)
            self.waitingStates.append(state)
        # 放されたとき
        if isinstance(event, KeyReleased):
            print("on_released")
            switch = event.switch
            for state in self.waitingStates:
                action = state.action
                if state.switch is switch:
                    self.do_release(action, state, now)
                    self.waitingStates.remove(state)

    def tick(self, now: int):
        for state in self.waitingStates:
            action = state.action
            if isinstance(action, HoldTapAction):
                if state.held(now):
                    hold = action.hold
                    if isinstance(hold, SingleKeyCode):
                        self.kbd.press(hold.key_code)
                        state.pressed_at = 0
                    if isinstance(hold, MultipleKeyCodes):
                        for code in hold.key_codes:
                            self.kbd.press(code.key_code)
                        state.pressed_at = 0

    def do_release(self, action: Action, state: WaitingState, now: int):
        if isinstance(action, SingleKeyCode):
            self.kbd.release(action.key_code)
        if isinstance(action, MultipleKeyCodes):
            for code in reversed(action.key_codes):
                self.kbd.release(code)
        if isinstance(action, HoldTapAction):
            if state.pressed_at == 0 or state.held(now):
                self.do_release(action.hold, state, now)
                print("released hold")
            else:
                self.do_release(action.tap, state, now)
                print("released tap")

    def find_action(self, switch: KeySwitch, layer: int) -> Action:
        if layer > 0:
            layer -= 1
            action = switch.action(layer)
            if isinstance(action, TransAction):
                return self.find_action(switch, layer)
            else:
                return action
        else:
            return NoOpAction()

    def set_layer(self, action: Action, held: bool):
        self.layer = 0
        if isinstance(action, LayerAction):
            self.layer = action.layer
        if isinstance(action, HoldTapAction):
            if held:
                self.set_layer(action.hold, held)
            else:
                self.set_layer(action.tap, held)
