from datetime import timedelta
from queue import Queue

from tqdm import tqdm

from enums import Symbol
from enums.indicators import RSI, MACD
from trader.Position import Position
from utils.cache import Cache

buys = Queue()  # FIXME add a number
sells = Queue()

# tqdm_list = [1]
signals_q = Queue()  # TODO put a limit

pb = tqdm([], colour='red')

indicators = {
    MACD: 1,  # priority stuffs
    RSI: .1
}

delayed_orders = Queue(10)

positions = [
    Position(Symbol("BTC"))
]

_ttl = timedelta(hours=10)
cache_positions = Cache(200)  # FIXME 200 positions
