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
            matrix: list[list[KeySwitch]],
            row_pins: list,
            col_pins: list,
            processor: Processor,
            settle_time: float = 0.001,
            active_low: bool = True,
            drive_inactive: bool = False,
            col_to_row: bool = False):
        super().__init__(EventQueue(), processor)
        self.col_to_row = col_to_row
        if col_to_row:
            self._validate_col_to_row(matrix, row_pins, col_pins)
            out_pins = col_pins
            in_pins = row_pins
        else:
            self._validate_row_to_col(matrix, row_pins, col_pins)
            out_pins = row_pins
            in_pins = col_pins

        self.matrix = matrix
        self.settle_time = settle_time
        self.active_low = active_low
        self.drive_inactive = drive_inactive
        self.selected_value = not active_low
        self.inactive_value = active_low

        self.out_pins = []
        for pin in out_pins:
            dio = digitalio.DigitalInOut(pin)
            self.out_pins.append(dio)
            self._deselect(dio)

        pull = digitalio.Pull.UP if active_low else digitalio.Pull.DOWN
        self.in_pins = []
        for pin in in_pins:
            dio = digitalio.DigitalInOut(pin)
            dio.switch_to_input(pull=pull)
            self.in_pins.append(dio)

    def scan(self):
        now = monotonic_ns() // 1000 // 1000

        for out_index, out_pin in enumerate(self.out_pins):
            self._select(out_pin)
            if self.settle_time > 0:
                sleep(self.settle_time)

            for in_index, in_pin in enumerate(self.in_pins):
                if self.col_to_row:
                    col_index = out_index
                    row_index = in_index
                    switch = self.matrix[col_index][row_index]
                else:
                    row_index = out_index
                    col_index = in_index
                    switch = self.matrix[row_index][col_index]

                event = switch.update(in_pin.value == self.selected_value)
                if isinstance(event, KeyPressed) or isinstance(event, KeyReleased):
                    self.event_queue.enqueue(event, now)
                    if self.col_to_row:
                        print(f"[{col_index},{row_index}]")
                    else:
                        print(f"[{row_index},{col_index}]")
            self._deselect(out_pin)

    def _select(self, pin):
        pin.switch_to_output(value=self.selected_value)

    def _deselect(self, pin):
        if self.drive_inactive:
            pin.switch_to_output(value=self.inactive_value)
        else:
            pin.switch_to_input()

    def deinit(self):
        for pin in self.out_pins:
            pin.deinit()

        for pin in self.in_pins:
            pin.deinit()

    def _validate_row_to_col(self, matrix, row_pins, col_pins):
        if len(matrix) != len(row_pins):
            raise ValueError("matrix row count must match row_pins")

        for row in matrix:
            if len(row) != len(col_pins):
                raise ValueError("matrix column count must match col_pins")

    def _validate_col_to_row(self, matrix, row_pins, col_pins):
        if len(matrix) != len(col_pins):
            raise ValueError("matrix column count must match col_pins")

        for col in matrix:
            if len(col) != len(row_pins):
                raise ValueError("matrix row count must match row_pins")
