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
from makbe.sender import Sender
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard


class BleSender(Sender):
    """Bluetooth LE HIDでキーコードを送出するクラス"""

    KEYBOARD_APPEARANCE = 961

    def __init__(
        self,
        name: str = "Makbe Keyboard",
        wait_for_connection: bool = False,
        clear_bonds: bool = False,
    ):
        if clear_bonds:
            self.clear_bonds()

        self.hid = HIDService()
        self.device_info = DeviceInfoService(
            software_revision=getattr(adafruit_ble, "__version__", ""),
            manufacturer="makbe",
        )

        self.advertisement = ProvideServicesAdvertisement(self.hid)
        self.advertisement.appearance = self.KEYBOARD_APPEARANCE
        self.scan_response = Advertisement()
        self.scan_response.complete_name = name

        self.ble = adafruit_ble.BLERadio()
        self.ble.name = name

        super().__init__(Keyboard(self.hid.devices))
        self.start_advertising()

        if wait_for_connection:
            self.wait_for_connection()

    def start_advertising(self):
        if not self.ble.connected and not getattr(self.ble, "advertising", False):
            print("BLE advertising")
            self.ble.start_advertising(self.advertisement, self.scan_response)

    def clear_bonds(self):
        import _bleio

        _bleio.adapter.erase_bonding()

    def wait_for_connection(self):
        while not self.ble.connected:
            pass

    def update(self):
        self.start_advertising()

    def press(self, key_code: int):
        if not self.ble.connected:
            self.start_advertising()
            return
        super().press(key_code)

    def release(self, key_code: int):
        if not self.ble.connected:
            self.start_advertising()
            return
        super().release(key_code)
