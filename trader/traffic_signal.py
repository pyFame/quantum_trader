# from asyncio import Queue

from queue import Queue

from enums import Symbol
from enums.position import SHORT, LONG
from trader.Position import Position
from trader.globals import buys, sells
from utils.thread import keepAlive

from trader.globals import buys, sells

positions = [

]

"""
q - that gets all the buys,sell signals going to be kafka q
"""

"""
q msg- 

key - BTC/USDT


"""

signals_queue = Queue(100)

positions_cache = {
    # "BTC/USDT": Position(symbol)
}


def handle_signals():
    msg = signals_queue.get()
    val = msg.val

    symbol = Symbol.loads(msg.key)

    # send_order to kafka


@keepAlive
def buying():
    short = SHORT
    long = LONG
    while True:
        p = buys.get()
        if short.sell_signal(p): closes.put([short.close(p), short])

        if long.disable_open:
            if short.quantity > 0 and short.entry_price < p: continue
            opens.put([long.open(self.AMOUNT, p), long])


class SignalHandler():

    @keepAlive
    def selling(self):
        short = self.SHORT
        long = self.LONG
        while 1:
            s = sells.get()
            if long.sell_signal(s):
                closes.put([long.close(s), long])

            if short.disable_open:
                if long.quantity > 0 and long.entry_price > s: continue
                opens.put([short.open(self.AMOUNT, s), short])
