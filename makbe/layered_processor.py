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
import action
from .key_event import KeyEvent, KeyReleased, KeyPressed
from .processor import Processor


class LayeredProcessor(Processor):
    """ WIP:レイヤとHoldTapに対応したプロセッサ
    タップダンスやマクロなどには対応していない
    """
    def __init__(self, kbd):
        self.layer = 0
        self.default_layer = 0
        self.waitingActions: [action.WaitingAction] = []
        self.kbd = kbd

    def put(self, event: KeyEvent, now: int):
        """
        :param event: 処理するイベント
        :param now: 現在時刻に相当する数値（ns単位）
        """
        # 押されたとき
        if isinstance(event, KeyPressed):
            self.on_pressed(event)
        # 放されたとき
        if isinstance(event, KeyReleased):
            self.on_released(event, now)

    def on_pressed(self, event: KeyPressed):
        # アクションの取り出し
        a = event.switch.action(self.layer)
        if isinstance(a, action.TransAction):
            a = event.switch.action(self.default_layer)
        # 単一キーコード: 普通にpress
        if isinstance(a, action.SingleKeyCode):
            self.kbd.press(a.key_codes())
        # 複数キーコード: key_codesをsend
        if isinstance(a, action.MultipleKeyCodes):
            self.kbd.send(a.key_codes())
        # レイヤ、デフォルトレイヤの切り替え
        if isinstance(a, action.LayerAction):
            self.layer = a.layer_no()
        if isinstance(a, action.DefaultLayer):
            self.default_layer = a.layer_no()
        # HoldTapは、保持しておく
        if isinstance(a, action.HoldTapAction):
            self.waitingActions.append(action.WaitingAction(a, event.switch))

    def on_released(self, event: KeyReleased, now: int):
        # アクションの取り出し
        a = event.switch.action(self.layer)
        if isinstance(a, action.TransAction):
            a = event.switch.action(self.default_layer)
        # 単一キーコード: 普通にrelease
        if isinstance(a, action.SingleKeyCode):
            self.kbd.release(a.key_codes())
        # レイヤーを戻す
        if isinstance(a, action.LayerAction):
            if self.layer == a.layer_no():
                self.layer = self.default_layer
        # HoldTap: 経過時間による
        if isinstance(a, action.HoldTapAction):
            for w in self.waitingActions:
                if w.switch == event.switch:
                    # 保持しておいたのを破棄
                    self.waitingActions.remove(w)
                    # 経過時間によってそれぞれ処理
                    if now > w.since + w.timeout:
                        self.on_released(w.hold, now)
                    else:
                        # Tap（押して放す）
                        self.on_pressed(w.tap)
                        self.on_released(w.tap, now)

    def tick(self, now):
        for w in self.waitingActions:
            # 時間経過していたら、holdをpress
            if now > w.since + w.timeout:
                self.on_pressed(w.hold)
                w.timeout = 0
