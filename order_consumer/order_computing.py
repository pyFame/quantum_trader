import json
from typing import Optional

from icecream import ic

from conf import client
from order_consumer.globals import order_q, pb_order

import logging as log

from dask import delayed

from order_consumer.order import Order
from utils.thread import keepAlive


@keepAlive
def order_computing():
    while True:
        o = order_q.get()

        try:
            _order = o.compute()
        except Exception as e:
            log.error(e)
            ic(e)
        else:
            ic(_order)
        finally:
            pb_order.update()
            # pb_order.refresh()


def callback(key, val):
    val = json.loads(val)

    order = val.get("order", None)

    log.info(order)

    if order is None:
        return  # shortcircuit

    delayed_order = Order(order)

    order_q.put(delayed_order)

    pb_order.total += 1
    pb_order.refresh()
