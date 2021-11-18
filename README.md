# makbe-py

CircuitPythonでキーボードファームウェアを実装するためのライブラリです。

まだまだ、buggyなアルファ版です。

## 使い方

* MCUにそれぞれに対応したCircuitPythonをインストールします。
* CircuitPythonのライブラリバンドルから、adafruit_hidをCircuitPythonのlibフォルダ直下にコピーします。
* このリポジトリのmakbeフォルダをCircuitPythonのlibフォルダ直下にコピーします。
* keyboard定義コード（ex. keyboard_column13ansi.py）をCircuitPythonのルートにコピーします。
* code.pyを必要に応じて修正した後、CircuitPythonのルートにコピーします。

## keyboard定義

### 命名規則

* keyboard定義コードは、keyboard_*.pyというファイル名にします（推奨）。

### スイッチの定義

* Layerクラスでレイヤ番号を定数として定義します（推奨）。
* Switchesクラスで、使用する全てのスイッチをインスタンス変数として定義します。
* 個々のインスタンス変数はKeySwitchクラスにレイヤー分（省略できないので、trans()）のActionを指定して、割り当てます。

### I/Oエクスパンダへの割付

* 適当な名称のクラス（キーボードクラスと呼ぶ）を作ります。
* キーボードクラスにSwitchesクラスのインスタンスを生成し、swというインスタンス変数に代入します。
* 使用するI/Oエクスパンダに合わせたクラス（ex. TCA9555, TCA9554）を生成し、上記のスイッチを割り付けます。
* 上記のI/Oエクスパンダオブジェクトをリストにまとめます。

### スキャナの生成

* I2Cマスタを生成します（作り方は、MCU毎に異なることがあるので使用するMCUに合わせます）。
* キーイベントプロセッサ（ex. LayeredProcessor, ModelessProcessor）を生成します。
* 前述のI/Oエクスパンダのリストと上記のオブジェクトを指定して、スキャナ（ex. I2CScanner 将来的には、MatrixScannerを作るかも）を生成します。

## キーボードのカスタマイズと実行

* code.pyでキーボード定期コードからキーボードクラスをimportします。
* 必要に応じて、キーボードクラスのsw変数経由で各スイッチをカスタマイズします（Actionの再割り当て）。
* 無限ループ内で、キーボードクラスのスキャナでスキャンし続けます。

