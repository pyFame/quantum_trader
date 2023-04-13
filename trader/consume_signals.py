from typing import List

from conf import alog
from enums import Symbol
from enums.Order import Order, LONG
from enums.indicators import BUY, SELL, Message_Signal
from enums.position import SHORT
from trader.Position import Position
from trader.globals import delayed_orders, pb, cache_positions
from trader.publish_orders import publish_order


def consume_signal(key: str, val: str):
    # alog.info(key, val)

    symbol = Symbol.Loads(key)

    positions = cache_positions.get(symbol)  # LONG,SHORT

    if positions is None:
        long = Position(symbol, LONG)
        short = Position(symbol, SHORT)
        positions = [long, short]

    long, short = positions

    signal_message = Message_Signal.Loads(val)
    low_price = signal_message.low
    high_price = signal_message.high

    buy_sell_signal = signal_message.signal

    quantity: float = .01

    orders: List[Order] = []

    if buy_sell_signal == BUY:
        if long.open_signal(low_price):
            o = long.open(quantity=quantity, price=low_price)
            orders.append(o)

        if short.close_signal(high_price):
            o = short.close()  # TOOO
            orders.append(o)

        # o = Order(symbol, CLOSE, SHORT, AMOUNT)
    elif buy_sell_signal == SELL:
        if long.close_signal(high_price):
            o = long.close(price=high_price)
            orders.append(o)

        if short.close_signal(high_price):
            o = short.close(price=high_price)  # TOOO
            orders.append(o)

        # o = Order(symbol, OPEN, SHORT, quantity)  # , profit=df_high)
    else:
        alog.warn(f"invalid signal - {buy_sell_signal}")
        return

    cache_positions.set(symbol, positions)

    for o in orders:
        d_o = publish_order(symbol, o)
        delayed_orders.put(d_o)

        pb.total += 1
        pb.refresh()
