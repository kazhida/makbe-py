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
from .key_code import KeyCode
from time import monotonic_ns


class Action:
    """ キーアクションの基底クラス
    実際のアクションはこのクラスを継承したクラスです。
    """

    def layer_no(self):
        """ レイヤに関係するのであれば、そのレイヤ番号を返す
        :return: None レイヤーは関係しない
        """
        return None

    def key_codes(self):
        """ キーコードに関係するのであれば、そのリストを返す
        :return: [] 空配列を返す
        """
        return []


class NoOpAction(Action):
    """ なにもしないアクション
    """

    def __init__(self):
        pass


class TransAction(Action):
    """ デフォルトレイヤのアクションを踏襲する
    """

    def __init__(self):
        pass


class SingleKeyCode(Action):
    """ 1つ分のキーコードを割り当てられたアクション
    """

    def __init__(self, code: KeyCode):
        """
        :param code: 割り当てるキーコード
        """
        self.code = code

    def key_codes(self):
        """
        :return: 割り当てられたキーコードをリストにして返す
        """
        return [self.code]


class MultipleKeyCodes(Action):
    """ 複数のキーコードを割り当てられたアクション
    """

    def __init__(self, codes: [KeyCode]):
        """
        :param codes: 割り当てるキーコードのリスト
        """
        self.codes = codes

    def key_codes(self):
        """
        :return: 割り当てられたキーコードのリストを返す
        """
        return self.codes


class LayerAction(Action):
    """ レイヤを切り替えるアクション
    """

    def __init__(self, layer: int):
        """
        :param layer: 割り当てるレイヤ番号
        """
        self.layer = layer

    def layer_no(self):
        """
        :return: 割り当てられたレイヤ番号を返す
        """
        return self.layer


class DefaultLayer(Action):
    """ デフォルトレイヤの切り替え
    """

    def __init__(self, layer: int):
        """
        :param layer: 割り当てるレイヤ番号
        """
        self.layer = layer

    def layer_no(self):
        """
        :return: 割り当てられたレイヤ番号
        """
        return self.layer


class HoldTapAction(Action):
    """ 特定時間押しっぱなしにした場合（hold）とそれ以前に話したとき(tap)、それぞれにアクションを割り当てるアクション
    """

    def __init__(self, hold: Action, tap: Action, timeout: int = 200):
        """
        :param hold: 押しっぱなしの場合のアクション
        :param tap: すぐに話したときのアクション
        :param timeout: holdかtapかを判別する時間（m秒単位）
        """
        self.hold = hold
        self.tap = tap
        self.timeout = timeout * 1000 * 1000


class WaitingAction(HoldTapAction):
    """ HoldTapActionに発生時刻を加えたもの
    """

    def __init__(self, hold_tap: HoldTapAction, switch: KeySwitch):
        super(WaitingAction, self).__init__(hold_tap.hold, hold_tap.tap, hold_tap.timeout)
        self.since = monotonic_ns()
        self.switch = switch


def k(kc: KeyCode) -> Action:
    """
    :param kc: キーコード
    :return: 割り当てられたキーコードのSingleKeyCodeアクションを返す
    """
    return SingleKeyCode(kc)


def m(km: KeyCode, kc: KeyCode) -> Action:
    """
    :param km: キーコード（モディファイア）
    :param kc: キーコード
    :return: 割り当てられたキーコードのSingleKeyCodeアクションを返す
    """
    mb = KeyCode.as_modifier_bit(km)
    return SingleKeyCode(mb | kc)


def multi(kcs: [KeyCode]) -> Action:
    """
    :param kcs:キーコードのリスト
    :return: 割り当てられたキーコードのMultipleKeyCodesアクションを返す
    """
    return MultipleKeyCodes(kcs)


def la(layer: int) -> Action:
    """
    :param layer: レイヤ番号
    :return: 割り当てられたレイヤ番号のLayerアクションを返す
    """
    return LayerAction(layer)


def d(layer: int) -> Action:
    """
    :param layer: レイヤ番号
    :return: 割り当てられたレイヤ番号のLayerアクションを返す
    """
    return DefaultLayer(layer)


def lt(layer:int, kc: KeyCode) -> Action:
    """
    :param layer: レイヤ番号
    :param kc: キーコード
    :return: holdでレイヤ切り替え、tapでキーコードのHoldTapアクションを返す
    """
    return HoldTapAction(la(layer), SingleKeyCode(kc))


def mt(modifier: KeyCode, kc: KeyCode) -> Action:
    """
    :param modifier: モディファイアキーのキーコード
    :param kc: キーコード
    :return: holdでモディファイア、taoでキーコードのHoldTapアクションを返す
    """
    return HoldTapAction(SingleKeyCode(modifier), SingleKeyCode(kc))
