
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
from makbe import KeyEvent, KeyPressed, KeyReleased
from makbe.processor import Processor
from makbe.actions import Action, HoldTapAction, SingleKeyCode, MultipleKeyCodes, TransAction, LayerAction, NoOpAction
from makbe.key_switch import KeySwitch


class WaitingState:

    def __init__(self, action: Action, switch: KeySwitch, pressed_at: int):
        self.action = action
        self.pressed_at = pressed_at
        self.switch = switch
        self.hold_activated = False  # ホールドアクションがアクティブかどうか
        self.activated_layer = None  # このキーで有効化されたレイヤー
        self.modifier_key = None     # このキーで有効化されたモディファイアキー

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
        self.active_modifiers = set()  # 現在アクティブなモディファイアキー
        self.active_layers = {}        # 現在アクティブなレイヤー (レイヤー番号: アクティブ化したWaitingStateのリスト)
        # ホールドアクションが有効になった後のキー入力のための状態追跡
        self.pending_layer_update = False
        self.last_update_time = 0

    def put(self, event: KeyEvent, now: int):
        """
        :param event: 処理するイベント
        :param now: 現在時刻に相当する数値（ms単位）
        """
        # pending_layer_updateフラグがあれば必ずレイヤー更新
        if self.pending_layer_update:
            self.update_layer(now)
            self.pending_layer_update = False
            self.last_update_time = now
        # 定期的なレイヤー更新判定
        elif now - self.last_update_time > 50:
            self.update_layer(now)
            self.last_update_time = now

        print("layer: %d" % self.layer)
        print(f"Active modifiers: {self.active_modifiers}")

        # 押されたとき
        if isinstance(event, KeyPressed):
            print("on_pressed")
            switch = event.switch
            action = switch.actions[self.layer]
            if isinstance(action, TransAction):
                action = self.find_action(switch, self.layer)

            # HoldTapActionの場合は、すぐに処理せず、状態を記録するだけ
            if isinstance(action, HoldTapAction):
                state = WaitingState(action, switch, now)
                self.waitingStates.append(state)
                return

            # 通常キーの処理
            if isinstance(action, SingleKeyCode):
                self.process_key_press(action.key_code)
            elif isinstance(action, MultipleKeyCodes):
                for code in action.key_codes:
                    self.process_key_press(code)
            elif isinstance(action, LayerAction):
                # レイヤーをアクティブにする
                layer_num = action.layer
                state = WaitingState(action, switch, now)
                state.activated_layer = layer_num

                if layer_num not in self.active_layers:
                    self.active_layers[layer_num] = []
                self.active_layers[layer_num].append(state)

                self.update_layer(now)
                self.waitingStates.append(state)
                return  # すでにWaitingStateを追加したので、以下の処理はスキップ

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
                    break

    def update_layer(self, now: int):
        """現在のアクティブなレイヤーに基づいて、現在のレイヤーを更新する"""
        # デフォルトはレイヤー0
        self.layer = 0

        # アクティブなレイヤーがある場合は、最小のレイヤー番号を使用（小さい番号が優先）
        if self.active_layers:
            self.layer = min(self.active_layers.keys())
            print(f"Active layers: {self.active_layers.keys()}, current layer: {self.layer}")

    def process_key_press(self, key_code: int):
        """キーコードの処理（モディファイアキーか通常キーかを判断）"""
        print(f"DEBUG: process_key_press called with key_code: {hex(key_code)}")
        if self.is_modifier(key_code):
            self.active_modifiers.add(key_code)
        self.kbd.press(key_code)

    def process_key_release(self, key_code: int):
        """キー解放の処理"""
        if self.is_modifier(key_code):
            self.active_modifiers.discard(key_code)
        self.kbd.release(key_code)

    def tick(self, now: int):
        # ホールドアクションがこのtick()で有効化されたかどうかをトラッキングするフラグ
        any_hold_activated = False

        for state in self.waitingStates:
            action = state.action
            if isinstance(action, HoldTapAction) and not state.hold_activated:
                # ホールド状態をチェック
                if state.held(now):
                    hold = action.hold
                    # ホールドアクションを処理（即時反映）
                    if isinstance(hold, LayerAction):
                        layer_num = hold.layer
                        state.activated_layer = layer_num
                        if layer_num not in self.active_layers:
                            self.active_layers[layer_num] = []
                        self.active_layers[layer_num].append(state)
                        self.update_layer(now)  # 直ちにレイヤ更新
                        any_hold_activated = True
                    elif isinstance(hold, SingleKeyCode) and self.is_modifier(hold.key_code):
                        # モディファイアキーの場合は即時press
                        self.process_key_press(hold.key_code)
                        state.modifier_key = hold.key_code
                        # キーボードレポートは自動的に送信される（reportメソッドは存在しない）
                        any_hold_activated = True
                    else:
                        self.activate_hold_action(hold)
                        any_hold_activated = True

                    # ホールドがアクティブになったことをマーク
                    state.hold_activated = True
                    print(f"hold activated: {type(hold).__name__}")

        # このtick()でホールドが有効化された場合、次のput()でレイヤー更新を確実に実行
        if any_hold_activated:
            self.pending_layer_update = True

    def activate_hold_action(self, action: Action):
        """ホールドアクションをアクティブ化する（レイヤーアクションを除く）"""
        if isinstance(action, SingleKeyCode):
            self.process_key_press(action.key_code)
        elif isinstance(action, MultipleKeyCodes):
            for code in action.key_codes:
                self.process_key_press(code)

    def do_press(self, action: Action):
        if isinstance(action, SingleKeyCode):
            self.process_key_press(action.key_code)
        elif isinstance(action, MultipleKeyCodes):
            for code in action.key_codes:
                self.process_key_press(code)
        elif isinstance(action, LayerAction):
            layer_num = action.layer
            if layer_num not in self.active_layers:
                self.active_layers[layer_num] = []
            # レイヤ自体の有効化は押下管理のWaitingStateにより行う

    def do_release(self, action: Action, state: WaitingState, now: int):
        # 状態に関連づけられたレイヤーがある場合、レイヤーをデアクティブにする
        if state.activated_layer is not None:
            layer_num = state.activated_layer
            if layer_num in self.active_layers:
                if state in self.active_layers[layer_num]:
                    self.active_layers[layer_num].remove(state)
                if not self.active_layers[layer_num]:
                    del self.active_layers[layer_num]
            print(f"Layer {layer_num} deactivated, current active layers: {list(self.active_layers.keys())}")
            self.pending_layer_update = True

        # モディファイアキーがアクティブな場合、解放する
        if state.modifier_key is not None:
            self.process_key_release(state.modifier_key)
            state.modifier_key = None

        # キーの解放処理
        if isinstance(action, SingleKeyCode):
            self.process_key_release(action.key_code)
        elif isinstance(action, MultipleKeyCodes):
            for code in reversed(action.key_codes):
                self.process_key_release(code)
        elif isinstance(action, HoldTapAction):
            if state.hold_activated:
                # ホールド状態が有効化されていた場合は、Tapは実行せず、Holdだけを解放する
                hold_action = action.hold
                # レイヤーアクションでなければ、かつ既にモディファイアとして処理されていなければ、キーを解放する
                if not isinstance(hold_action, LayerAction) and state.modifier_key is None:
                    if isinstance(hold_action, SingleKeyCode):
                        self.process_key_release(hold_action.key_code)
                    elif isinstance(hold_action, MultipleKeyCodes):
                        for code in reversed(hold_action.key_codes):
                            self.process_key_release(code)
                print("released hold")
            else:
                # ホールド状態になる前に離された場合のみタップアクションを実行
                self.do_press(action.tap)
                self.do_release(action.tap, state, now)
                if isinstance(action.tap, SingleKeyCode):
                    print("released tap %d" % action.tap.key_code)
                else:
                    print("released tap")

        # レイヤー状態を更新
        self.update_layer(now)

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

    def is_modifier(self, key_code: int):
        # モディファイアキーのキーコードのリスト
        modifiers = [
            0xE0,  # LEFT_CONTROL
            0xE1,  # LEFT_SHIFT
            0xE2,  # LEFT_ALT
            0xE3,  # LEFT_GUI (Windows/Command key)
            0xE4,  # RIGHT_CONTROL
            0xE5,  # RIGHT_SHIFT
            0xE6,  # RIGHT_ALT
            0xE7,  # RIGHT_GUI
        ]
        return key_code in modifiers