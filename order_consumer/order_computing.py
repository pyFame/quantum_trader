import json

from icecream import ic

from conf import alog
from utils.thread import keepAlive
from order_consumer.globals import order_q, pb_order
from order_consumer.order import Order


@keepAlive
def order_computing():
    while True:
        o = order_q.get()

        try:
            _order = o.compute()
        except Exception as e:
            alog.error(e)
        else:
            ic(_order)
        finally:
            pb_order.update()
            # pb_order.refresh()


def callback(key: str, val: str):
    val = json.loads(val)

    order = val.get("order", None)

    alog.info(order)

    if order is None:
        alog.debug("received invalid order")
        return  # shortcircuit

    delayed_order = Order(order)

    order_q.put(delayed_order)

    pb_order.total += 1
    pb_order.refresh()
