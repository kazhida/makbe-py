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
from .action import Action, Trans, NoOp, HoldTap, MultipleKeyCodes, Layer
from .key_code import KeyCode
from .key_event import EventQueue, KeyEvent, EventSince, EventIterator, KeyReleased, KeyPressed
from .key_state import KeyState, NormalKeyState, LayerModifierState
from .key_switch import KeySwitch
from .processor import Processor
from .waiting_state import WaitingState


class LayeredProcessor(Processor):
    """標準的なプロセッサ
    レイヤとHoldTapに対応。
    タップダンスやマクロなどには対応していない
    Keyberonからのベタ移植なので、仕組みはまだ分かっていない(^^;
    """
    def __init__(self, kbd):
        self.states: [KeyState] = []
        self.waiting: WaitingState = WaitingState.empty()
        self.stacked = EventQueue(16)
        self.kbd = kbd

    def put(self, event: KeyEvent):
        """
        :param event: 処理するイベント
        """
        push_backed = self.stacked.push(event)
        if push_backed is not None:
            self.waiting.do_hold(lambda a, s, d: self.do_action(a, s, d))
            self.unstack(push_backed)
        # waiting_stateにあれば、waiting_into_tap()へ
        if self.waiting.is_corresponding_release(event):
            self.waiting.do_tap(lambda a, s, d: self.do_action(a, s, d))
        self.send_codes()

    def tick(self):
        # statesを正規化して、それぞれにtick()
        self.states = filter(lambda st: st is not None, self.states)
        for s in EventIterator(self.stacked):
            s.tick()
        if self.waiting.is_not_empty():
            if self.waiting.tick():
                self.waiting.do_hold(lambda a, s, d: self.do_action(a, s, d))
        else:
            s = self.stacked.pop()
            if s is not None:
                self.unstack(s)
        self.send_codes()

    def unstack(self, stacked: EventSince):
        if isinstance(stacked.event, KeyReleased):
            self.states = filter(lambda s: s is not None, map(lambda s: s.release(stacked.event.switch), self.states))
        if isinstance(stacked.event, KeyPressed):
            action = self.press_as_action(stacked.event.switch, self.current_layer())
            self.do_action(action, stacked.event.switch, stacked.since)

    def send_codes(self):
        codes = []
        for s in self.states:
            kc = s.key_code
            if kc is not None:
                codes.append(kc)
        self.kbd.send(codes)

    def current_layer(self) -> int:
        layers = filter(lambda ly: ly is not None, map(lambda st: st.get_layer, self.states))
        layer = 0
        for la in layers:
            layer += la
        return layer

    def press_as_action(self, switch: KeySwitch, layer: int) -> Action:
        action = switch.action(layer)
        if action is Trans:
            if layer > 0:
                return self.press_as_action(switch, layer - 1)
            else:
                return NoOp()
        else:
            return action

    def do_action(self, action: Action, switch: KeySwitch, delay: int):

        if action is KeyCode:
            self.states.append(NormalKeyState(action.key_codes()[0], switch))

        if action is MultipleKeyCodes:
            for kc in action.key_codes():
                self.states.append(NormalKeyState(kc, switch))

        if action is Layer:
            self.states.append(LayerModifierState(action.layer(), switch))

        if action is HoldTap:
            hold_tap: HoldTap = action
            hold = hold_tap.hold
            tap = hold_tap.tap
            timeout = hold_tap.timeout
            self.waiting = WaitingState(switch, timeout - delay, hold, tap)
            for event in EventIterator(self.stacked):
                if self.waiting.is_corresponding_release(event):
                    if timeout < delay - event.since:
                        self.waiting.do_hold(lambda a, s, d: self.do_action(a, s, d))
                    else:
                        self.waiting.do_tap(lambda a, s, d: self.do_action(a, s, d))
