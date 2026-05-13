# makbe-py

CircuitPythonでキーボードファームウェアを実装するためのライブラリです。

まだまだ、buggyなアルファ版です。

## 概要

makbe-pyは、I2C接続のI/Oエクスパンダでキースイッチを読み取り、USB HIDまたはBluetooth LE HIDでキーコードを送信するためのキーボードコントローラーです。

主な構成は次の通りです。

* `code.py`: CircuitPython起動時に実行されるエントリポイント
* `keyboard_*.py`: キーボードごとの配列、レイヤー、I/Oエクスパンダ割り当て
* `makbe/`: スキャナ、プロセッサ、キーアクション、キーコード、送信クラス
* `makbe/sender.py`: USB/BLEなどのキーコード送信処理

現在の `code.py` では `keyboard_card_pendant.py` の `CardPendant` を起動しています。

## 使い方

1. MCUに対応したCircuitPythonをインストールします。
2. CircuitPythonのライブラリバンドルから、`adafruit_hid` をCircuitPythonの `lib` フォルダ直下にコピーします。
3. BLEを使う場合は、同じくライブラリバンドルから、`adafruit_ble` もCircuitPythonの `lib` フォルダ直下にコピーします。
4. このリポジトリの `makbe` フォルダをCircuitPythonの `lib` フォルダ直下にコピーします。
5. 使用するkeyboard定義コード、例: `keyboard_card_pendant.py` や `keyboard_column13ansi.py` をCircuitPythonのルートにコピーします。
6. `code.py` を必要に応じて修正した後、CircuitPythonのルートにコピーします。

## 実行の流れ

`code.py` はキーボードクラスを生成し、無限ループでスキャナを更新します。

```python
from keyboard_card_pendant import CardPendant
from time import sleep

sleep(0.5)
print("start!")

keyboard = CardPendant()
print("started")

while True:
    keyboard.scanner.update()
    sleep(0.001)
```

処理の流れは次の通りです。

```text
code.py
  -> keyboard.scanner.update()
  -> I2CScanner がI/Oエクスパンダを読む
  -> KeyPressed / KeyReleased イベントを生成
  -> LayeredProcessor がレイヤーやHoldTapを処理
  -> Sender / BleSender が press() / release() を送信
```

## keyboard定義

### 命名規則

keyboard定義コードは、`keyboard_*.py` というファイル名にします。

例:

* `keyboard_card_pendant.py`
* `keyboard_column7ansi.py`
* `keyboard_column13ansi.py`
* `keyboard_column13ansi_w.py`

### スイッチの定義

`Layer` クラスでレイヤ番号を定数として定義します。

```python
class Layer:
    QWERTY = 0
    FUNCS = 1
```

`Switches` クラスで、使用する全てのスイッチをインスタンス変数として定義します。

```python
class Switches:
    def __init__(self):
        self.kb_h = KeySwitch([
            lt(Layer.FUNCS, KC.KB_H),
            trans()
        ])
        self.kb_j = KeySwitch([
            kc(KC.KB_J),
            mc(KC.L_GUI, KC.KB_X)
        ])
```

個々の `KeySwitch` には、レイヤー分の `Action` を指定します。何もしない、または下位レイヤーを踏襲したい場合は `trans()` を指定します。

### Action

よく使うActionヘルパーは次の通りです。

* `kc(key_code)`: 単一キーコード
* `mc(modifier, key_code)`: モディファイア付きキー。例: `mc(KC.L_GUI, KC.KB_C)`
* `lt(layer, key_code)`: 長押しでレイヤー、短押しでキー
* `mt(modifier, key_code)`: 長押しでモディファイア、短押しでキー
* `trans()`: 下位レイヤーのアクションを踏襲

キーコードは `makbe/key_code.py` の `KeyCode` を使います。keyboard定義内では、短く書くために次のように `KC` を作っています。

```python
class KC(KeyCode):
    pass
```

## I/Oエクスパンダへの割り付け

キーボードクラスを作り、`Switches` のインスタンスを `self.sw` に入れます。

```python
self.sw = Switches()
self.expanders = []
```

使用するI/Oエクスパンダに合わせたクラスを生成し、ピンにスイッチを割り付けます。

```python
expander = PCA9536()
expander.assign(0, self.sw.kb_h)
expander.assign(1, self.sw.kb_j)
expander.assign(2, self.sw.kb_k)
expander.assign(3, self.sw.kb_l)
self.expanders.append(expander)
```

現在用意されている主なI/Oエクスパンダは次の通りです。

* `TCA9555`: 16ピン。`TCA9555(0x00)` はI2Cアドレス `0x20`
* `TCA9554`: 8ピン。`TCA9554(0x00)` はI2Cアドレス `0x20`
* `PCA9536`: 4ピン。現在はI2Cアドレス `0x41` 固定

## スキャナの生成

I2Cマスタ、キーイベントプロセッサ、スキャナを生成します。

```python
i2c = I2C(SCL, SDA)
while not i2c.try_lock():
    pass

kbd = Keyboard(usb_hid.devices)
proc = LayeredProcessor(Sender(kbd))

self.scanner = I2CScanner(self.expanders, i2c, proc)
```

`I2CScanner` は、I/Oエクスパンダを読み、キー状態の変化を `KeyPressed` / `KeyReleased` としてプロセッサに渡します。

## キーコードの送信

キーコード送信は `makbe/sender.py` の `Sender` 系クラスが担当します。

### USB HID

USBで送信する場合は、CircuitPythonの `usb_hid.devices` から `Keyboard` を作り、`Sender` に渡します。

```python
import usb_hid
from adafruit_hid.keyboard import Keyboard
from makbe.sender import Sender

kbd = Keyboard(usb_hid.devices)
proc = LayeredProcessor(Sender(kbd))
```

デバッグ出力を見たい場合は `WrappedKeyboard` を挟めます。

```python
kbd = WrappedKeyboard(Keyboard(usb_hid.devices))
proc = LayeredProcessor(Sender(kbd))
```

### Bluetooth LE HID

Bluetoothで送信する場合は `BleSender` を使います。

```python
from makbe.sender import BleSender

proc = LayeredProcessor(BleSender(name="Makbe Keyboard"))
```

起動時に接続されるまで待ちたい場合は、`wait_for_connection=True` を指定します。

```python
proc = LayeredProcessor(
    BleSender(name="Makbe Keyboard", wait_for_connection=True)
)
```

`BleSender` は内部でBLE HIDの `Keyboard` を作り、接続済みなら `press()` / `release()` をBluetooth LE HID経由で送信します。未接続時は広告を開始して、その入力は送信せず戻ります。

BLEを使う場合は、MCUがBLEに対応している必要があります。また、CircuitPythonの `lib` に `adafruit_ble` と `adafruit_hid` が必要です。

## キーボードのカスタマイズと実行

`code.py` で使用したいキーボードクラスをimportします。

```python
from keyboard_card_pendant import CardPendant

keyboard = CardPendant()
```

別のキーボード定義を使う場合は、importと生成箇所を差し替えます。

```python
from keyboard_column13ansi_w import Column13ansiW

keyboard = Column13ansiW()
```

キーマップのカスタマイズは、キーボードクラス生成後に `keyboard.sw` 経由で行います。

```python
# 例:
# keyboard.sw.esc.append_action(kc(KeyCode.GRAVE))
```

最後に、無限ループ内でスキャナを更新し続けます。

```python
while True:
    keyboard.scanner.update()
    sleep(0.001)
```

## I2Cデバイスの確認

次のようなエラーが出る場合があります。

```text
OSError: [Errno 19] No such device
```

これは、指定されたI2CアドレスにI/Oエクスパンダが見つからない場合に発生します。例えば `PCA9536` は現在 `0x41` 固定なので、`0x41` にデバイスが見つからないと初期化に失敗します。

CircuitPython REPLでI2Cスキャンを実行してください。

```python
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass

print([hex(addr) for addr in i2c.scan()])
```

結果の見方:

* `[]`: 配線、電源、GND、SCL/SDA、プルアップ抵抗、使用ピンを確認します。
* `['0x41']`: `PCA9536` は見えています。リセット後に再実行してください。
* `0x41` 以外: 実際のアドレスに合わせてエクスパンダ側のアドレス設定を確認します。

TCA9555/TCA9554の場合、`TCA9555(0x00)` や `TCA9554(0x00)` は `0x20`、`0x01` は `0x21` です。

## トラブルシュート

### USBでキーが出ない

* `adafruit_hid` が `lib` に入っているか確認します。
* keyboard定義側で `Keyboard(usb_hid.devices)` と `Sender(kbd)` を使っているか確認します。
* `WrappedKeyboard` を挟むと、`pressed xxh` / `released xxh` のログでprocessorまで届いているか確認できます。

### BLEでキーが出ない

* MCUがBLE対応か確認します。
* `adafruit_ble` と `adafruit_hid` が `lib` に入っているか確認します。
* PCやスマートフォン側で `"Makbe Keyboard"` など指定した名前のBLE HIDデバイスをペアリングします。
* 未接続時のキー入力は送信されません。接続後にキー入力してください。

### `OSError: [Errno 19] No such device`

I2Cデバイスが見つかっていません。上の「I2Cデバイスの確認」を実行し、期待するアドレスが見えているか確認します。

## ライセンス

MIT License
