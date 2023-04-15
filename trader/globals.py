from queue import Queue

from enums import Symbol
from enums.Order import LONG
from enums.indicators import RSI, MACD
from trader.Position import Position
from utils.cache import Cache
from utils.progress_bar import ProgressBar

buys = Queue()  # FIXME add a number
sells = Queue()

# tqdm_list = [1]
signals_q = Queue()  # TODO put a limit

pb = ProgressBar(color="#36D7B7")

indicators = {
    MACD: 1,  # priority stuffs
    RSI: .1
}

delayed_orders = Queue(10)

positions = [
    Position(Symbol("BTC"), LONG)
]

# _ttl = timedelta(hours=10)
cache_positions = Cache(maxsize=200)  # FIXME 200 positions
