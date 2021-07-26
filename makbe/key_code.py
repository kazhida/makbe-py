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

from enum import IntEnum, auto


class KeyCode(IntEnum):
    # The "no" key, a placeholder to express nothing.
    No = 0x00
    # Error if too much keys are pressed at the same time.
    ErrorRollOver = auto()
    # The POST fail error.
    PostFail = auto()
    # An undefined error occurred.
    ErrorUndefined = auto()
    # `a` and `A`.
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()
    # `1` and `!`.
    Kb1 = auto()
    # `2` and `@`.
    Kb2 = auto()
    # `3` and `#`.
    Kb3 = auto()
    # `4` and `$`.
    Kb4 = auto()
    # `5` and `%`.
    Kb5 = auto()
    # `6` and `^`.
    Kb6 = auto()
    # `7` and `&`.
    Kb7 = auto()
    # `8` and `*`.
    Kb8 = auto()
    # `9` and `(`.
    Kb9 = auto()
    # `0` and `)`.
    Kb0 = auto()
    Enter = auto()
    Escape = auto()
    BSpace = auto()
    Tab = auto()
    Space = auto()
    # `-` and `_`.
    Minus = auto()
    # `=` and `+`.
    Equal = auto()
    # `[` and `{`.
    LBracket = auto()
    # `]` and `}`.
    RBracket = auto()
    # `\` and `|`.
    Bslash = auto()
    # Non-US `#` and `~` (Typically near the Enter key).
    NonUsHash = auto()
    # `;` and `:`.
    SColon = auto()
    # `'` and `"`.
    Quote = auto()
    # How to have ` as code?
    # \` and `~`.
    Grave = auto()
    # `,` and `<`.
    Comma = auto()
    # `.` and `>`.
    Dot = auto()
    # `/` and `?`.
    Slash = auto()
    CapsLock = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    PScreen = auto()
    ScrollLock = auto()
    Pause = auto()
    Insert = auto()
    Home = auto()
    PgUp = auto()
    Delete = auto()
    End = auto()
    PgDown = auto()
    Right = auto()
    Left = auto()
    Down = auto()
    Up = auto()
    NumLock = auto()
    # Keypad `/`
    KpSlash = auto()
    # Keypad `*`
    KpAsterisk = auto()
    # Keypad `-`.
    KpMinus = auto()
    # Keypad `+`.
    KpPlus = auto()
    # Keypad enter.
    KpEnter = auto()
    # Keypad 1.
    Kp1 = auto()
    Kp2 = auto()
    Kp3 = auto()
    Kp4 = auto()
    Kp5 = auto()
    Kp6 = auto()
    Kp7 = auto()
    Kp8 = auto()
    Kp9 = auto()
    Kp0 = auto()
    KpDot = auto()
    # Non-US `\` and `|` (Typically near the Left-Shift key)
    NonUsBslash = auto()
    Application = auto()
    # not a key, used for errors
    Power = auto()
    # Keypad `=`.
    KpEqual = auto()
    F13 = auto()
    F14 = auto()
    F15 = auto()
    F16 = auto()
    F17 = auto()
    F18 = auto()
    F19 = auto()
    F20 = auto()
    F21 = auto()
    F22 = auto()
    F23 = auto()
    F24 = auto()
    Execute = auto()
    Help = auto()
    Menu = auto()
    Select = auto()
    Stop = auto()
    Again = auto()
    Undo = auto()
    Cut = auto()
    Copy = auto()
    Paste = auto()
    Find = auto()
    Mute = auto()
    VolUp = auto()
    VolDown = auto()
    # Deprecated.
    LockingCapsLock = auto()
    # Deprecated.
    LockingNumLock = auto()
    # Deprecated.
    LockingScrollLock = auto()
    # Keypad `,`, also used for the brazilian keypad period (.) key.
    KpComma = auto()
    # Used on AS/400 keyboard
    KpEqualSign = auto()
    Intl1 = auto()
    Intl2 = auto()
    Intl3 = auto()
    Intl4 = auto()
    Intl5 = auto()
    Intl6 = auto()
    Intl7 = auto()
    Intl8 = auto()
    Intl9 = auto()
    Lang1 = auto()
    Lang2 = auto()
    Lang3 = auto()
    Lang4 = auto()
    Lang5 = auto()
    Lang6 = auto()
    Lang7 = auto()
    Lang8 = auto()
    Lang9 = auto()
    AltErase = auto()
    SysReq = auto()
    Cancel = auto()
    Clear = auto()
    Prior = auto()
    Return = auto()
    Separator = auto()
    Out = auto()
    Oper = auto()
    ClearAgain = auto()
    CrSel = auto()
    ExSel = auto()
    # According to QMK, 0xA5-0xDF are not usable on modern keyboards
    # Modifiers
    # Left Control.
    LCtrl = 0xE0
    # Left Shift.
    LShift = auto()
    # Left Alt.
    LAlt = auto()
    # Left GUI (the Windows key).
    LGui = auto()
    # Right Control.
    RCtrl = auto()
    # Right Shift.
    RShift = auto()
    # Right Alt (or Alt Gr).
    RAlt = auto()
    # Right GUI (the Windows key).
    RGui = auto()
    # Unofficial
    MediaPlayPause = 0xE8
    MediaStopCD = auto()
    MediaPreviousSong = auto()
    MediaNextSong = auto()
    MediaEjectCD = auto()
    MediaVolUp = auto()
    MediaVolDown = auto()
    MediaMute = auto()
    MediaWWW = auto()
    MediaBack = auto()
    MediaForward = auto()
    MediaStop = auto()
    MediaFind = auto()
    MediaScrollUp = auto()
    MediaScrollDown = auto()
    MediaEdit = auto()
    MediaSleep = auto()
    MeidaCoffee = auto()
    MediaRefresh = auto()
    MediaCalc = auto()

    def is_modifier(self):
        return KeyCode.LCtrl <= self <= KeyCode.RGui

    def as_modifier_bit(self):
        if self.is_modifier():
            return 1 << (self - KeyCode.LCtrl)
        else:
            return 0
