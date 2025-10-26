# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from .key_event import KeyPressed, KeyReleased
from .io_expander import IoExpander
from .processor import Processor
from .scanner import Scanner
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
        for d in expanders:
            d.init_device(i2c)

    def scan(self):
        """
        I/Oエクスパンダをスキャンして、プロセッサに渡す
        """
        now = monotonic_ns() // 1000 // 1000
        for d in self.expanders:
            for i, p in enumerate(d.read_device(self.i2c)):
                switch = d.switch(i)
                event = switch.update(p)
                if isinstance(event, KeyPressed):
                    self.processor.put(event, now)
                if isinstance(event, KeyReleased):
                    self.processor.put(event, now)
        self.processor.tick(now)
