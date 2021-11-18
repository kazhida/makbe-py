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

class Action:
    """ キーアクションの基底クラス
    実際のアクションはこのクラスを継承したクラスです。
    """


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

    def __init__(self, key_code: int):
        """
        :param key_code: 割り当てるキーコード
        """
        self.key_code = key_code


class MultipleKeyCodes(Action):
    """ 複数のキーコードを割り当てられたアクション
    """

    def __init__(self, key_codes: [int]):
        """
        :param key_codes: 割り当てるキーコードのリスト
        """
        self.key_codes = key_codes


class LayerAction(Action):
    """ レイヤを切り替えるアクション
    """

    def __init__(self, layer: int):
        """
        :param layer: 割り当てるレイヤ番号
        """
        self.layer = layer


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
        self.timeout = timeout


def kc(key_code: int) -> Action:
    """
    :param key_code: キーコード
    :return: 割り当てられたキーコードのSingleKeyCodeアクションを返す
    """
    return SingleKeyCode(key_code)


def mc(modifier: int, key_code: int) -> Action:
    """
    モディファイア修飾したキー
    :param modifier: キーコード（モディファイア）
    :param key_code: キーコード
    :return: 割り当てられたキーコードのSingleKeyCodeアクションを返す
    """
    return MultipleKeyCodes([modifier, key_code])


def la(layer: int) -> Action:
    """
    :param layer: レイヤ番号
    :return: 割り当てられたレイヤ番号のLayerアクションを返す
    """
    return LayerAction(layer)


def lt(layer: int, key_code: int) -> Action:
    """
    長押しでレイヤ指定、短押しでキーコード
    :param layer: レイヤ番号
    :param key_code: キーコード
    :return: holdでレイヤ切り替え、tapでキーコードのHoldTapアクションを返す
    """
    return HoldTapAction(la(layer), SingleKeyCode(key_code))


def mt(modifier: int, key_code: int) -> Action:
    """
    長押しでモディファイア、短押しでキーコード
    :param modifier: モディファイアキーのキーコード
    :param key_code: キーコード
    :return: holdでモディファイア、tapでキーコードのHoldTapアクションを返す
    """
    return HoldTapAction(SingleKeyCode(modifier), SingleKeyCode(key_code))


def trans() -> Action:
    return TransAction()
