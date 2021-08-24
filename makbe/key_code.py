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

class KeyCode:
    """キーコード
    CircuitPythonにadafruit_hid.keyboard.KeyCodeがあるが、
    ここではCircuitPythonに依存したくないので、独自に定義している
    """

    # The "no" key, a placeholder to express nothing.
    NO = 0x00
    # Error if too much keys are pressed at the same time.
    ERROR_ROLL_OVER = 0x01
    # The POST fail error.
    POST_FAIL = 0x02
    # An undefined error occurred.
    ERROR_UNDEFINED = 0x03
    # `a` and `A`.
    KB_A = 0x04
    KB_B = 0x05
    KB_C = 0x06
    KB_D = 0x07
    KB_E = 0x08
    KB_F = 0x09
    KB_G = 0x0a
    KB_H = 0x0b
    KB_I = 0x0c
    KB_J = 0x0d
    KB_K = 0x0e
    KB_L = 0x0f
    KB_M = 0x10
    KB_N = 0x11
    KB_O = 0x12
    KB_P = 0x13
    KB_Q = 0x14
    KB_R = 0x15
    KB_S = 0x16
    KB_T = 0x17
    KB_U = 0x18
    KB_V = 0x19
    KB_W = 0x1A
    KB_X = 0x1B
    KB_Y = 0x1C
    KB_Z = 0x1D
    # `1` and `!`.
    KB_1 = 0x1E
    # `2` and `@`.
    KB_2 = 0x1F
    # `3` and `#`.
    KB_3 = 0x20
    # `4` and `$`.
    KB_4 = 0x21
    # `5` and `%`.
    KB_5 = 0x22
    # `6` and `^`.
    KB_6 = 0x23
    # `7` and `&`.
    KB_7 = 0x24
    # `8` and `*`.
    KB_8 = 0x25
    # `9` and `(`.
    KB_9 = 0x26
    # `0` and `)`.
    KB_0 = 0x27
    ENTER = 0x28
    ESCAPE = 0x29
    BACK_SPACE = 0x2A
    TAB = 0x2B
    SPACE = 0x2C
    # `-` and `_`.
    MINUS = 0x2D
    # `=` and `+`.
    EQUAL = 0x2E
    # `[` and `{`.
    L_BRACKET = 0x2F
    # `]` and `}`.
    R_BRACKET = 0x30
    # `\` and `|`.
    BACK_SLASH = 0x31
    # Non-US `#` and `~` (Typically near the Enter key).
    NON_US_HASH = 0x32
    # `;` and `:`.
    SEMI_COLON = 0x33
    # `'` and `"`.
    QUOTE = 0x34
    # How to have ` as code?
    # \` and `~`.
    GRAVE = 0x35
    # `,` and `<`.
    COMMA = 0x36
    # `.` and `>`.
    DOT = 0x37
    # `/` and `?`.
    SLASH = 0x38
    CAPS_LOCK = 0x39
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
    PRINT_SCREEN = 0x46
    SCROLL_LOCK = 0x47
    PAUSE = 0x48
    INSERT = 0x49
    HOME = 0x4A
    PAGE_UP = 0x4B
    DELETE = 0x4C
    END = 0x4D
    PAGE_DOWN = 0x4E
    RIGHT = 0x4F
    LEFT = 0x50
    DOWN = 0x51
    UP = 0x52
    NUM_LOCK = 0x53
    # Keypad `/`
    KP_SLASH = 0x54
    # Keypad `*`
    KP_ASTERISK = 0x55
    # Keypad `-`.
    KP_MINUS = 0x56
    # Keypad `+`.
    KP_PLUS = 0x57
    # Keypad enter.
    KP_ENTER = 0x58
    # Keypad 1.
    KP_1 = 0x59
    KP_2 = 0x5A
    KP_3 = 0x5B
    KP_4 = 0x5C
    KP_5 = 0x5D
    KP_6 = 0x5E
    KP_7 = 0x5F
    KP_8 = 0x60
    KP_9 = 0x61
    KP_0 = 0x62
    KP_DOT = 0x63
    # Non-US `\` and `|` (Typically near the Left-Shift key)
    NON_US_BK_SLASH = 0x64
    APPLICATION = 0x65
    # not a key, used for errors
    POWER = 0x66
    # Keypad `=`.
    KP_EQUAL = 0x67
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
    EXECUTE = 0x74
    HELP = 0x75
    MENU = 0x76
    SELECT = 0x77
    STOP = 0x78
    AGAIN = 0x79
    UNDO = 0x7A
    CUT = 0x7B
    COPY = 0x7C
    PASTE = 0x7D
    FIND = 0x7E
    MUTE = 0x7F
    VOLUME_UP = 0x80
    VOLUME_DOWN = 0x81
    # Deprecated.
    LOCKING_CAPS_LOCK = 0x82
    # Deprecated.
    LOCKING_NUM_LOCK = 0x83
    # Deprecated.
    LOCKING_SCROLL_LOCK = 0x84
    # Keypad `,`, also used for the brazilian keypad period (.) key.
    KP_COMMA = 0x85
    # Used on AS/400 keyboard
    KP_EQUAL_SIGN = 0x86
    INTL_1_RO = 0x87
    INTL_2_KATAKANAHIRAGANA = 0x88
    INTL_3_YEN = 0x89
    INTL_4_HENKAN = 0x8A
    INTL_5_MUHENKAN = 0x8B
    INTL_6_KPJPCOMMA = 0x8C
    INTL_7 = 0x8D
    INTL_8 = 0x8E
    INTL_9 = 0x8F
    LANG_1 = 0x90
    LANG_2 = 0x91
    LANG_3 = 0x92
    LANG_4 = 0x93
    LANG_5 = 0x94
    LANG_6 = 0x95
    LANG_7 = 0x96
    LANG_8 = 0x97
    LANG_9 = 0x98
    ALT_ERASE = 0x99
    SYS_REQ = 0x9A
    CANCEL = 0x9B
    CLEAR = 0x9C
    PRIOR = 0x9D
    RETURN = 0x9E
    SEPARATOR = 0x9F
    OUT = 0xA0
    OPER = 0xA1
    CLEAR_AGAIN = 0xA2
    CR_SEL = 0xA3
    EX_SEL = 0xA4
    # According to QMK, 0xA5-0xDF are not usable on modern keyboards
    # Modifiers
    # Left Control.
    L_CTRL = 0xE0
    # Left Shift.
    L_SHIFT = 0xE1
    # Left Alt.
    L_ALT = 0xE2
    # Left GUI (the Windows key).
    L_GUI = 0xE3
    # Right Control.
    R_CTRL = 0xE4
    # Right Shift.
    R_SHIFT = 0xE5
    # Right Alt (or Alt Gr).
    R_ALT = 0xE6
    # Right GUI (the Windows key).
    R_GUI = 0xE7
    # Unofficial
    MEDIA_PLAY_PAUSE = 0xE8
    MEDIA_STOP_CD = 0xE9
    MEDIA_PREVIOUS_SONG = 0xEA
    MEDIA_NEXT_SONG = 0xEB
    MEDIA_EJECT_CD = 0xEC
    MEDIA_VOLUME_UP = 0xED
    MEDIA_VOLUME_DOWN = 0xEE
    MEDIA_MUTE = 0xEF
    MEDIA_WWW = 0xF0
    MEDIA_BACK = 0xF1
    MEDIA_FORWARD = 0xF2
    MEDIA_STOP = 0xF3
    MEDIA_FIND = 0xF4
    MEDIA_SCROLL_UP = 0xF5
    MEDIA_SCROLL_DOWN = 0xF6
    MEDIA_EDIT = 0xF7
    MEDIA_SLEEP = 0xF8
    MEDIA_COFFEE = 0xF9
    MEDIA_REFRESH = 0xFA
    MEDIA_CALC = 0xFB

    @staticmethod
    def is_modifier(key_code: int):
        return KeyCode.L_CTRL <= key_code <= KeyCode.R_GUI

    @staticmethod
    def as_modifier_bit(key_code: int):
        if KeyCode.is_modifier(key_code):
            return 1 << (key_code - KeyCode.L_CTRL)
        else:
            return 0
