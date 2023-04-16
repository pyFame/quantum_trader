import datetime as dt
from datetime import timedelta

from dask import compute
from icecream import ic

from conf.kafka import TOPIC_ORDERS
from enums import Symbol
from enums.Order import Order
from lib.kafka import Kafka, KafkaMessage
from trader import alog
from trader.globals import delayed_orders, pb
from utils import Time
from utils.thread import keepAlive

kafka_client = Kafka()


def delivery_order(err: str, msg: object) -> None:
    if err is not None:
        err_msg = f'Message delivery failed: {err}'
        alog.error(err_msg)
    else:
        ic(msg)
        alog.info(f'message delivered to {msg.topic()} [{msg.partition()}]')

    # pb_kafka.update(1)
    pb.update(1)


@keepAlive
def handle_delayed_orders():
    alog.info("starting handle_delayed_orders")
    while True:
        d_order = delayed_orders.get()
        compute(d_order)
        # pb_order.update() #added to callback
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
    # pb.update(1)

    kafka_client.publish(msg, callback=delivery_order)  # TODO: add a callback
    # pb_kafka.add(1)
