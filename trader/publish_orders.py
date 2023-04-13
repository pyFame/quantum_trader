import datetime as dt
from datetime import timedelta

from dask import compute

from conf.kafka import TOPIC_ORDERS
from enums import Symbol
from enums.Order import Order
from lib.kafka import Kafka, KafkaMessage
from trader import alog
from trader.globals import delayed_orders, pb
from utils import Time
from utils.thread import keepAlive

kafka_client = Kafka()


@keepAlive
def handle_delayed_orders():
    alog.info("starting handle_delayed_orders")
    while True:
        d_order = delayed_orders.get()
        compute(d_order)
        pb.update()
        # d_order.compute()


# @delayed
def publish_order(symbol: Symbol, o: Order):
    now_: dt.datetime = Time.now(timedelta())
    key = symbol
    val = {
        "created_at": now_.timestamp(),
        "expired_at": now_.timestamp(),
        "created": str(now_),
        "order": o.binance_order,
    }
    msg = KafkaMessage(TOPIC_ORDERS, key, val)

    kafka_client.publish(msg)  # TODO: add a callback
