import datetime as dt
from datetime import timedelta
from queue import Queue

from dask import delayed

from conf import alog
from conf.kafka import TOPIC_ORDERS
from enums import Symbol
from enums.Order import Order
from lib.kafka import Kafka, KafkaMessage
from utils import Time
from utils.thread import keepAlive

delayed_orders = Queue(10)

kafka_client = Kafka()


@keepAlive
def handle_delayed_orders():
    alog.info("started handle_delayed_orders")
    while True:
        d_order = delayed_orders.get()
        d_order.compute()


@delayed
def publish_order(symbol: Symbol, o: Order):
    now_: dt.datetime = Time.now(timedelta())

    key = symbol.json
    val = {
        "created_at": now_.timestamp(),
        "created": str(now_),
        "order": o.json,
    }
    msg = KafkaMessage(TOPIC_ORDERS, symbol)

    kafka_client.publish(msg)  # TODO: add a callback
