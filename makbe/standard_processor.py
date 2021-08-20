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
from typing import cast
from .action import Action, Trans, NoOp, HoldTap, MultipleKeyCodes, Layer
from .key_code import KeyCode
from .key_event import EventQueue, KeyEvent, EventSince, EventIterator, KeyReleased, KeyPressed
from .key_state import KeyState, NormalKey, LayerModifier
from .key_switch import KeySwitch
from .processor import Processor
from .waiting_state import WaitingState


class StandardProcessor(Processor):
    """標準的なプロセッサ
    レイヤとHoldTapに対応。
    タップダンスやマクロなどには対応していない

    Keyberonからのベタ移植なので、仕組みはまだ分かっていない(^^;

    Attributes
    ----------
    states:

    waiting:

    stacked:

    """

    def __init__(self):
        self.states: [KeyState] = []
        self.waiting: [WaitingState] = []
        self.stacked = EventQueue(16)

    def put(self, event: KeyEvent):
        """
        :param event: 処理するイベント
        """
        # stackedに格納。あふれたものは、waiting_into_hold()へ
        push_backed = self.stacked.push(event)
        if push_backed is not None:
            self.waiting_into_hold()
            self.unstack(push_backed)
        # waiting_stateにあれば、waiting_into_tap()へ
        waiting_state = self.waiting_state_or_none()
        if waiting_state and waiting_state.is_corresponding_release:
            self.waiting_into_tap()

    def tick(self):
        # statesを正規化して、それぞれにtick()
        self.states = filter(lambda st: st is not None, self.states)
        for s in EventIterator(self.stacked):
            s.tick()

        waiting_state = self.waiting_state_or_none()
        if waiting_state:
            self.waiting_into_tap()
        if waiting_state is None:
            stacked = self.stacked.pop()
            if stacked is not None:
                self.unstack(stacked)
        else:
            if waiting_state.tick():
                self.waiting_into_hold()
        return self.keycodes()

    def waiting_state_or_none(self):
        if self.waiting.count(WaitingState) > 0:
            # waiting_stateがあればそれを返す
            return self.waiting[0]
        else:
            # 無ければ、Noneを返す
            return None

    def waiting_into_hold(self):
        waiting_state = self.waiting_state_or_none()
        if waiting_state:
            hold = waiting_state.hold
            switch = waiting_state.switch
            self.waiting.clear()
            self.do_action(hold, switch, 0)

    def waiting_into_tap(self):
        waiting_state = self.waiting_state_or_none()
        if waiting_state:
            tap = waiting_state.tap
            switch = waiting_state.switch
            self.waiting.clear()
            self.do_action(tap, switch, 0)

    def unstack(self, stacked: EventSince):

        if isinstance(stacked.event, KeyReleased):
            self.states = filter(lambda s: s is not None, map(lambda s: s.release(stacked.event.switch), self.states))

        if isinstance(stacked.event, KeyPressed):
            action = self.press_as_action(stacked.event.switch, self.current_layer())
            self.do_action(action, stacked.event.switch, stacked.since)

    def keycodes(self):
        return filter(lambda s: s is not None, map(lambda s: s.key_code, self.states))

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
            self.states.append(NormalKey(action.key_codes()[0], switch))

        if action is MultipleKeyCodes:
            for kc in action.key_codes():
                self.states.append(NormalKey(kc, switch))

        if action is Layer:
            self.states.append(LayerModifier(action.layer(), switch))

        if action is HoldTap:
            hold_tap = cast(HoldTap, action)
            hold = hold_tap.hold
            tap = hold_tap.tap
            timeout = hold_tap.timeout
            self.waiting = WaitingState(switch, timeout - delay, hold, tap)
            for event in EventIterator(self.stacked):
                if self.waiting.is_corresponding_release(event):
                    if timeout < delay - event.since:
                        self.waiting_into_hold()
                    else:
                        self.waiting_into_tap()
