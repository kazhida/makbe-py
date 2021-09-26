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

from .action import Action, TransAction, NoOpAction
from .key_event import KeyEvent, KeyPressed, KeyReleased


class Debouncer:
    """KeySwitchが使うチャタリング防止機構
    """

    def __init__(self, limit: int):
        """規定回数を指定してオブジェクトを生成
        :param limit: チャタリングではないと判定する回数
        """
        self.current = False
        self.pressed = False
        self.count = 0
        self.limit = limit

    def update(self, pressed: bool) -> bool:
        """状態更新
        :param pressed: ピンの状態（ONならTrue）
        :return: 変化があったらTrue
        """
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
    """キースイッチ
    アクションは複数レイヤに対応するため、アクションのリストで保持している

    Attributes
    ----------
    action:
        対応するアクション（最下層に割り当てられる）
    default:
        未指定レイヤを使われたときのアクション
    debounce:
        チャタリング防止の回数
    """

    def __init__(self, actions: [Action],
                 default: Action = TransAction(),
                 debounce: int = 2):
        """
        :param actions: 対応するアクション（最下層に割り当てられる）
        :param default: 未指定レイヤを使われたときのアクション
        :param debounce: チャタリング防止の回数
        """
        self.actions = actions
        self.default_action = default
        self.debouncer = Debouncer(debounce)

    def update(self, pressed: bool) -> KeyEvent:
        """状態更新
        :param pressed: ピンの状態（ONならTrue）
        :return: 変化が無ければ、KeyPressedでもKeyReleasedでもないKeyEventを返す。変化があればそのイベントを返す。
        """
        if not self.debouncer.update(pressed):
            return KeyEvent(self)
        elif self.debouncer.current:
            return KeyPressed(self)
        else:
            return KeyReleased(self)

    def action(self, layer: int) -> Action:
        """
        :param layer: レイヤ番号
        :return: 指定されたレイヤのアクションを返す
        """
        if layer < len(self.actions):
            return self.actions[layer]
        else:
            return self.default_action

    def append_action(self, action: Action):
        """
        :param action: 追加するアクション
        :return: 自分自身を返す（メソッドチェイン用）
        """
        self.actions.append(action)
        return self

    def append_actions(self, actions: [Action]):
        """
        :param actions: 追加するアクション
        :return: 自分自身を返す（メソッドチェイン用）
        """
        for a in actions:
            self.actions.append(a)
        return self


    def remove_layers(self, remove_all: bool = False):
        """レイヤに割り当てられたアクションの除去
        キーマップのカスタマイズに使用する
        :param remove_all: 最下層のアクションも削除する
        :return: 自分自身を返す（メソッドチェイン用）
        """
        if remove_all:
            self.actions.clear()
        else:
            while len(self.actions) > 1:
                self.actions.pop()
        return self


def nop_switch() -> KeySwitch:
    """
    :return: 何もしないキースイッチ（デフォルト値用）
    """
    return KeySwitch(NoOpAction(), NoOpAction())


EMPTY_SWITCH = KeySwitch(NoOpAction(), NoOpAction())