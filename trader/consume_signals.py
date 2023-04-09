from conf import alog
from enums import Symbol
from enums.Order import Order, CLOSE, OPEN
from enums.indicators import BUY, SELL, Message_Signal
from enums.position import SHORT
from trader.publish_orders import publish_order, delayed_orders


def consume_signal(key: str, val: str):
    alog.info(key, val)

    symbol = Symbol.Loads(key)

    signal_message = Message_Signal.Loads(val)

    signal = signal_message.signal

    o: Order = None

    AMOUNT: float = .01

    if signal == BUY:
        o = Order(symbol, CLOSE, SHORT, AMOUNT)
    elif signal == SELL:
        o = Order(symbol, OPEN, SHORT, AMOUNT)  # , profit=df_high)
    else:
        alog.warn(f"invalid signal - {signal}")
        return

    d_o = publish_order(symbol, o)
    delayed_orders.put(d_o)
