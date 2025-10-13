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
from makbe.key_event import KeyPressed, KeyReleased
from makbe.io_expander import IoExpander
from makbe.processor import Processor
from makbe.scanner import Scanner
from time import monotonic_ns
from collections import deque
try:
    from typing import Optional, List, Any, Tuple, Union, Deque
except ImportError:
    # CircuitPythonランタイムでは型ヒントをスキップ
    pass


class I2CScanner(Scanner):
    """I2Cを使用したスキャナ
    moduloアーキテクチャに基づいたスキャナ
    非同期動作をサポートするイベントキューベースの実装
    """

    def __init__(self, expanders: List[IoExpander], i2c: Any, processor: Processor,
                 time_provider=monotonic_ns, debug: bool = False, scan_interval_ms: int = 5,
                 event_queue_size: int = 32):
        """
        :param expanders: I/Oエクスパンダのリスト
        :param i2c: I2Cマスタ
        :param processor: キーイベントを処理するオブジェクト
        :param time_provider: 時間を返す関数（ns単位）。テスト容易性のために注入可能
        :param debug: デバッグログ出力の有効化
        :param scan_interval_ms: スキャン間の最小間隔（ミリ秒）
        :param event_queue_size: イベントキューの最大サイズ
        """
        self.processor = processor
        self.expanders = expanders
        self.i2c = i2c
        self.time_provider = time_provider
        self.debug = debug
        self.scan_interval_ms = scan_interval_ms
        self.last_scan_time_ns = 0
        self.last_process_time_ns = 0
        self.process_interval_ms = 1  # プロセッサ更新間隔（ms）
        
        # イベントキュー: (イベント, 時間) のタプルを格納
        self.event_queue = deque([], event_queue_size)
        
        # 各デバイスの初期化（各デバイスは独立して処理、失敗したデバイスがあっても続行）
        for d in expanders:
            try:
                ok = d.init_device(i2c)
                if not ok and self.debug:
                    print(f"I2CScanner: デバイス初期化失敗: {d}")
            except Exception as e:
                if self.debug:
                    print(f"I2CScanner: デバイス初期化例外: {d} - {e}")

    def scan(self):
        """
        I/Oエクスパンダをスキャンする (古いインターフェース用)
        update()を呼び出すだけ
        """
        self.update()
        
    def update(self) -> bool:
        """
        状態を更新し、スキャンとイベント処理を非同期に行う
        メインループで頻繁に呼び出す必要がある
        
        :return: 何らかの処理（スキャンまたはイベント処理）が行われた場合はTrue
        """
        now_ns = self.time_provider()
        did_something = False
        
        # スキャン処理（キー読み取り）
        if self._should_scan(now_ns):
            self._do_scan(now_ns)
            did_something = True
            
        # イベント処理（キューからプロセッサへ）
        if self._should_process(now_ns):
            self._process_events(now_ns)
            did_something = True
            
        return did_something
        
    def _should_scan(self, now_ns: int) -> bool:
        """スキャンすべきタイミングかどうか判定"""
        elapsed_ms = (now_ns - self.last_scan_time_ns) // 1000000
        return elapsed_ms >= self.scan_interval_ms
        
    def _should_process(self, now_ns: int) -> bool:
        """イベント処理すべきタイミングかどうか判定"""
        if not self.event_queue:  # キューが空なら処理不要
            return False
            
        elapsed_ms = (now_ns - self.last_process_time_ns) // 1000000
        return elapsed_ms >= self.process_interval_ms
        
    def _do_scan(self, now_ns: int):
        """I/Oエクスパンダをスキャンして、イベントをキューに追加する"""
        self.last_scan_time_ns = now_ns
        
        try:
            # 各エクスパンダを独立してスキャン
            for d in self.expanders:
                readings = None
                try:
                    readings = d.read_device(self.i2c)
                except Exception as e:
                    if self.debug:
                        print(f"I2CScanner: デバイス読取失敗: {d} - {e}")
                    continue
                
                if readings is None:
                    continue
                    
                # 各ピンの状態を処理
                for i, pin_state in enumerate(readings):
                    try:
                        switch = d.switch(i)
                        event = switch.update(pin_state)
                        
                        # 有効なイベントのみキューに追加
                        if isinstance(event, KeyPressed) or isinstance(event, KeyReleased):
                            self.event_queue.append((event, now_ns))
                            if self.debug and len(self.event_queue) == self.event_queue.maxlen:
                                print(f"I2CScanner: イベントキューが一杯です")
                    except Exception as e:
                        if self.debug:
                            print(f"I2CScanner: キースイッチ処理エラー: ピン {i}, デバイス {d} - {e}")
                        continue
                        
        except Exception as e:
            if self.debug:
                print(f"I2CScanner: スキャン全体エラー: {e}")
                
    def _process_events(self, now_ns: int):
        """キューからイベントを取り出してプロセッサに渡す"""
        self.last_process_time_ns = now_ns
        
        try:
            # キューが空になるまで、または最大処理数に達するまで処理
            max_events_per_cycle = 5  # 一度に処理するイベントの最大数
            events_processed = 0
            
            while self.event_queue and events_processed < max_events_per_cycle:
                event, timestamp = self.event_queue.popleft()
                try:
                    self.processor.put(event, timestamp)
                    events_processed += 1
                except Exception as e:
                    if self.debug:
                        print(f"I2CScanner: プロセッサイベント処理エラー: {e}")
            
            # 全イベントの処理後、tickを呼び出す
            if events_processed > 0:
                self.processor.tick(now_ns)
                
        except Exception as e:
            if self.debug:
                print(f"I2CScanner: イベント処理全体エラー: {e}")
