from queue import Queue

from tqdm import tqdm

from enums.indicators import RSI, MACD

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
