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

from enum import IntEnum


class KeyCode(IntEnum):
    # The "no" key, a placeholder to express nothing.
    No = 0x00
    # Error if too much keys are pressed at the same time.
    ErrorRollOver = 0x01
    # The POST fail error.
    PostFail = 0x02
    # An undefined error occurred.
    ErrorUndefined = 0x03
    # `a` and `A`.
    A = 0x04
    B = 0x05
    C = 0x06
    D = 0x07
    E = 0x08
    F = 0x09
    G = 0x0a
    H = 0x0b
    I = 0x0c
    J = 0x0d
    K = 0x0e
    L = 0x0f
    M = 0x10
    N = 0x11
    O = 0x12
    P = 0x13
    Q = 0x14
    R = 0x15
    S = 0x16
    T = 0x17
    U = 0x18
    V = 0x19
    W = 0x1A
    X = 0x1B
    Y = 0x1C
    Z = 0x1D
    # `1` and `!`.
    Kb1 = 0x1E
    # `2` and `@`.
    Kb2 = 0x1F
    # `3` and `#`.
    Kb3 = 0x20
    # `4` and `$`.
    Kb4 = 0x21
    # `5` and `%`.
    Kb5 = 0x22
    # `6` and `^`.
    Kb6 = 0x23
    # `7` and `&`.
    Kb7 = 0x24
    # `8` and `*`.
    Kb8 = 0x25
    # `9` and `(`.
    Kb9 = 0x26
    # `0` and `)`.
    Kb0 = 0x27
    Enter = 0x28
    Escape = 0x29
    BSpace = 0x2A
    Tab = 0x2B
    Space = 0x2C
    # `-` and `_`.
    Minus = 0x2D
    # `=` and `+`.
    Equal = 0x2E
    # `[` and `{`.
    LBracket = 0x2F
    # `]` and `}`.
    RBracket = 0x30
    # `\` and `|`.
    BSlash = 0x31
    # Non-US `#` and `~` (Typically near the Enter key).
    NonUsHash = 0x32
    # `;` and `:`.
    SColon = 0x33
    # `'` and `"`.
    Quote = 0x34
    # How to have ` as code?
    # \` and `~`.
    Grave = 0x35
    # `,` and `<`.
    Comma = 0x36
    # `.` and `>`.
    Dot = 0x37
    # `/` and `?`.
    Slash = 0x38
    CapsLock = 0x39
    F1 = 0x3A
    F2 = 0x3B
    F3 = 0x3C
    F4 = 0x3D
    F5 = 0x3E
    F6 = 0x3F
    F7 = 0x40
    F8 = 0x41
    F9 = 0x42
    F10 = 0x43
    F11 = 0x44
    F12 = 0x45
    PScreen = 0x46
    ScrollLock = 0x47
    Pause = 0x48
    Insert = 0x49
    Home = 0x4A
    PgUp = 0x4B
    Delete = 0x4C
    End = 0x4D
    PgDown = 0x4E
    Right = 0x4F
    Left = 0x50
    Down = 0x51
    Up = 0x52
    NumLock = 0x53
    # Keypad `/`
    KpSlash = 0x54
    # Keypad `*`
    KpAsterisk = 0x55
    # Keypad `-`.
    KpMinus = 0x56
    # Keypad `+`.
    KpPlus = 0x57
    # Keypad enter.
    KpEnter = 0x58
    # Keypad 1.
    Kp1 = 0x59
    Kp2 = 0x5A
    Kp3 = 0x5B
    Kp4 = 0x5C
    Kp5 = 0x5D
    Kp6 = 0x5E
    Kp7 = 0x5F
    Kp8 = 0x60
    Kp9 = 0x61
    Kp0 = 0x62
    KpDot = 0x63
    # Non-US `\` and `|` (Typically near the Left-Shift key)
    NonUsBslash = 0x64
    Application = 0x65
    # not a key, used for errors
    Power = 0x66
    # Keypad `=`.
    KpEqual = 0x67
    F13 = 0x68
    F14 = 0x69
    F15 = 0x6A
    F16 = 0x6B
    F17 = 0x6C
    F18 = 0x6D
    F19 = 0x6E
    F20 = 0x6F
    F21 = 0x70
    F22 = 0x71
    F23 = 0x72
    F24 = 0x73
    Execute = 0x74
    Help = 0x75
    Menu = 0x76
    Select = 0x77
    Stop = 0x78
    Again = 0x79
    Undo = 0x7A
    Cut = 0x7B
    Copy = 0x7C
    Paste = 0x7D
    Find = 0x7E
    Mute = 0x7F
    VolUp = 0x80
    VolDown = 0x81
    # Deprecated.
    LockingCapsLock = 0x82
    # Deprecated.
    LockingNumLock = 0x83
    # Deprecated.
    LockingScrollLock = 0x84
    # Keypad `,`, also used for the brazilian keypad period (.) key.
    KpComma = 0x85
    # Used on AS/400 keyboard
    KpEqualSign = 0x86
    Intl1_RO = 0x87
    Intl2_KATAKANAHIRAGANA = 0x88
    Intl3_YEN = 0x89
    Intl4_HENKAN = 0x8A
    Intl5_MUHENKAN = 0x8B
    Intl6_KPJPCOMMA = 0x8C
    Intl7 = 0x8D
    Intl8 = 0x8E
    Intl9 = 0x8F
    Lang1 = 0x90
    Lang2 = 0x91
    Lang3 = 0x92
    Lang4 = 0x93
    Lang5 = 0x94
    Lang6 = 0x95
    Lang7 = 0x96
    Lang8 = 0x97
    Lang9 = 0x98
    AltErase = 0x99
    SysReq = 0x9A
    Cancel = 0x9B
    Clear = 0x9C
    Prior = 0x9D
    Return = 0x9E
    Separator = 0x9F
    Out = 0xA0
    Oper = 0xA1
    ClearAgain = 0xA2
    CrSel = 0xA3
    ExSel = 0xA4
    # According to QMK, 0xA5-0xDF are not usable on modern keyboards
    # Modifiers
    # Left Control.
    LCtrl = 0xE0
    # Left Shift.
    LShift = 0xE1
    # Left Alt.
    LAlt = 0xE2
    # Left GUI (the Windows key).
    LGui = 0xE3
    # Right Control.
    RCtrl = 0xE4
    # Right Shift.
    RShift = 0xE5
    # Right Alt (or Alt Gr).
    RAlt = 0xE6
    # Right GUI (the Windows key).
    RGui = 0xE7
    # Unofficial
    MediaPlayPause = 0xE8
    MediaStopCD = 0xE9
    MediaPreviousSong = 0xEA
    MediaNextSong = 0xEB
    MediaEjectCD = 0xEC
    MediaVolUp = 0xED
    MediaVolDown = 0xEE
    MediaMute = 0xEF
    MediaWWW = 0xF0
    MediaBack = 0xF1
    MediaForward = 0xF2
    MediaStop = 0xF3
    MediaFind = 0xF4
    MediaScrollUp = 0xF5
    MediaScrollDown = 0xF6
    MediaEdit = 0xF7
    MediaSleep = 0xF8
    MeidaCoffee = 0xF9
    MediaRefresh = 0xFA
    MediaCalc = 0xFB

    def is_modifier(self):
        return KeyCode.LCtrl <= self <= KeyCode.RGui

    def as_modifier_bit(self):
        if self.is_modifier():
            return 1 << (self - KeyCode.LCtrl)
        else:
            return 0
