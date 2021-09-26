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
from time import monotonic_ns


class KeyEvent(object):
    """キーイベントの基底クラス
    KeyPressedとKeyReleasedがこれを継承している
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        self.switch = switch

    def is_pressed(self) -> bool:
        """
        :return: KeyPressedイベントならTrueを返す
        """
        return False

    def is_released(self) -> bool:
        """
        :return: KeyReleasedイベントならTrueを返す
        """
        return False


class KeyPressed(KeyEvent):
    """キーが押されたときのイベント
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        super().__init__(switch)

    def is_pressed(self) -> bool:
        """
        :return: Trueを返す
        """
        return True


class KeyReleased(KeyEvent):
    """キーが話されたときのイベント
    """

    def __init__(self, switch):
        """
        :param switch: 割り当てるキースイッチ
        """
        super().__init__(switch)

    def is_released(self) -> bool:
        """
        :return: Trueを返す
        """
        return True


class EventSince:
    """キーイベントとそこからの経過時間（スキャン回数）の組み合わせ
    """

    def __init__(self, event: KeyEvent):
        """
        :param event: キーイベント
        """
        self.event = event
        self.since = monotonic_ns()
