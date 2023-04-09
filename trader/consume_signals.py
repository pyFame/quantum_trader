import json
from typing import Final

from conf import alog
from conf.kafka import TOPIC_SIGNALS
from enums import Symbol
from enums.indicators import BUY, SELL, Message_Signal
from enums.order import Order, CLOSE, OPEN
from enums.position import SHORT
from lib.kafka import Kafka, ConsumerProperties, LATEST
from trader.publish_orders import publish_order, delayed_orders, handle_delayed_orders


def consume_signal(key: str, val: str):
    alog.info(key, val)

    symbol = Symbol.Parse(key)

    message_args = json.loads(val)
    signal_message = Message_Signal(**message_args)

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
