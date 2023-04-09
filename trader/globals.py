from queue import Queue
from tqdm import tqdm

from enums.indicators import RSI, MACD
from lib.kafka import Kafka

buys = Queue()  # FIXME add a number
sells = Queue()

# tqdm_list = [1]
signals_q = Queue()  # TODO put a limit

# progress bar
pb_order = tqdm([], colour='green')  # iter(order_q.queue)
# pb_order.total=1
pb = pb_order

indicators = {
    MACD: 1,  # priority stuffs
    RSI: .1
}
