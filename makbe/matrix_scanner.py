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
import digitalio

from time import monotonic_ns, sleep

from makbe import Scanner, Processor, KeyPressed, KeyReleased, KeySwitch, EventQueue


class MatrixScanner(Scanner):

    def __init__(
            self,
            row2col: bool,
            matrix: list[list[KeySwitch]],
            row_pins: list[digitalio.Pin],
            col_pins: list[digitalio.Pin],
            processor: Processor,
            settle_time: float = 0.001,
            active_low: bool = True,
            debug: bool = False,
            drive_inactive: bool = False):
        super().__init__(EventQueue(), processor)
        self.settle_time = settle_time
        self.active_low = active_low
        self.active_value = not active_low
        self.inactive_value = active_low
        self.debug = debug
        self.drive_inactive = drive_inactive

        if row2col:
            self.scan_direction = "row2col"
            self.scan_matrix = matrix
            self.out_pin_sources = row_pins
            self.in_pin_sources = col_pins
        else:
            self.scan_direction = "col2row"
            self.scan_matrix = [list(row) for row in zip(*matrix)]
            self.out_pin_sources = col_pins
            self.in_pin_sources = row_pins

        self.out_pins = [digitalio.DigitalInOut(pin) for pin in self.out_pin_sources]
        self.in_pins = [digitalio.DigitalInOut(pin) for pin in self.in_pin_sources]

        for pin in self.out_pins:
            if drive_inactive:
                pin.direction = digitalio.Direction.OUTPUT
                pin.value = self.inactive_value
            else:
                pin.direction = digitalio.Direction.INPUT

        for pin in self.in_pins:
            pin.direction = digitalio.Direction.INPUT
            if active_low:
                pin.pull = digitalio.Pull.UP
            else:
                pin.pull = digitalio.Pull.DOWN

        if self.debug:
            print("MatrixScanner init")
            print("  direction:", self.scan_direction)
            print("  active_low:", self.active_low)
            print("  active_value:", self.active_value)
            print("  inactive_value:", self.inactive_value)
            print("  drive_inactive:", self.drive_inactive)
            print("  out_pins:", self.out_pin_sources)
            print("  in_pins:", self.in_pin_sources)
            print("  matrix:", len(self.scan_matrix), "x", len(self.scan_matrix[0]) if self.scan_matrix else 0)
            for index, pin in enumerate(self.in_pins):
                print("  idle in", index, self.in_pin_sources[index], "value", pin.value)

    def scan(self):
        now = monotonic_ns() // 1000 // 1000

        for out_index, row in enumerate(self.scan_matrix):
            out_pin = self.out_pins[out_index]
            out_pin.direction = digitalio.Direction.OUTPUT
            out_pin.value = self.active_value
            if self.debug:
                print(
                    "activate out",
                    out_index,
                    self.out_pin_sources[out_index],
                    "=",
                    self.active_value,
                    "active_low",
                    self.active_low)
            sleep(self.settle_time)

            for in_index, switch in enumerate(row):
                in_pin = self.in_pins[in_index]
                value = in_pin.value
                pressed = value != self.active_low
                if self.debug:
                    print(
                        "  read",
                        "out", out_index,
                        "in", in_index,
                        "pin", self.in_pin_sources[in_index],
                        "value", value,
                        "pressed", pressed)
                # スイッチにin_pinの状態を渡してイベントを取得
                event = switch.update(pressed)
                if isinstance(event, KeyPressed) or isinstance(event, KeyReleased):
                    if self.debug:
                        print("  event", type(event).__name__, "out", out_index, "in", in_index)
                    self.event_queue.enqueue(event, now)

            if self.drive_inactive:
                out_pin.value = self.inactive_value
            else:
                out_pin.direction = digitalio.Direction.INPUT
            if self.debug:
                print(
                    "deactivate out",
                    out_index,
                    self.out_pin_sources[out_index],
                    "=",
                    self.inactive_value if self.drive_inactive else "Hi-Z")

    def deinit(self):
        for pin in self.out_pins:
            pin.deinit()

        for pin in self.in_pins:
            pin.deinit()
