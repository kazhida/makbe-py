
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from .key_event import KeyPressed, KeyReleased
from .io_expander import IoExpander
from .processor import Processor
from .scanner import Scanner
from .event_queue import EventQueue
from time import monotonic_ns


class I2CScanner(Scanner):
    """I2Cを使用したスキャナ
    moduloアーキテクチャに基づいたスキャナ
    """

    def __init__(self, expanders: [IoExpander], i2c, processor: Processor):
        """
        :param expanders: I/Oエクスパンダのリスト
        :param i2c: I2Cマスタ
        :param processor: キーイベントを処理するオブジェクト
        """
        self.processor = processor
        self.expanders = expanders
        self.i2c = i2c
        self.event_queue = EventQueue()
        for d in expanders:
            d.init_device(i2c)

    def scan(self):
        """
        I/Oエクスパンダをスキャンして、キューに渡す
        """
        now = monotonic_ns() // 1000 // 1000

        # キューを使った並行処理モード
        for d in self.expanders:
            for i, p in enumerate(d.read_device(self.i2c)):
                switch = d.switch(i)
                event = switch.update(p)
                if isinstance(event, KeyPressed) or isinstance(event, KeyReleased):
                    self.event_queue.enqueue(event, now)

    def process_events(self):
        """
        キューに溜まったイベントをプロセッサで処理する
        """
        now = monotonic_ns() // 1000 // 1000

        # キューから全てのイベントを処理
        while not self.event_queue.is_empty():
            item = self.event_queue.dequeue()
            if item is not None:
                event, timestamp = item
                self.processor.put(event, timestamp)

        # 最後にtickを呼び出す
        self.processor.tick(now)

    def update(self):
        """
        スキャンとイベント処理を両方実行（統合モード）
        """
        self.scan()
        self.process_events()