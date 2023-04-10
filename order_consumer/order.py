from typing import Union

import pandas as pd
from binance.exceptions import BinanceAPIException
from dask import delayed
from icecream import ic

from conf import client, alog
from conf.kafka import TOPIC_ORDERS_DLQ
from lib.kafka import Kafka, KafkaMessage

kafka_client = Kafka()


@delayed
def Order(req_json: dict, return_type=pd.DataFrame) -> Union[pd.DataFrame, dict, None]:  # d is the json request

    d = req_json

    ic(f"order - {d}")

    try:
        _order: dict = client.futures_create_order(**d)
    except BinanceAPIException as e:
        alog.error(f"Order creation failed for order with error code {e.code}: {e.message} ...{d}")

        key = d["symbol"]
        val = {
            "code": e.code,
            "message": e.message,
            "order": d,
        }

        msg = KafkaMessage(TOPIC_ORDERS_DLQ, key, val)
        kafka_client.publish(msg)
        return
    except Exception as e:
        alog.error(f"order failed due to - {e}")
        return

    df = pd.DataFrame(_order, index=[0]).rename(columns={"": "position"})
    df.drop(['status', 'clientOrderId', 'avgPrice', 'executedQty', 'cumQty', 'cumQuote', 'timeInForce', 'reduceOnly',
             'workingType', 'priceProtect', 'origType', 'updateTime'], axis=1, inplace=True)

    ncol = ['activatePrice', 'origQty', 'price', 'priceRate', 'stopPrice']
    for i in ncol:  # convert numeric cols
        if i in df.columns: df[i] = pd.to_numeric(df[i])

    if return_type == dict:
        only_order = df.iloc[0].to_dict()  # Since only one order there is no need for a dataframe
        return only_order

    return df

# @delayed
# def order(order: dict) -> Optional[dict]:  # FIXME: deprecate and use order()
#     order_res = None
#
#     try:
#         order_res = client.futures_create_order(**order)
#     except Exception as e:
#         if hasattr(e, 'code'):
#             log.error(order_res)
#             log.error(f"@order {e.code} {e.message}")
#         else:
#             log.exception(f'@order {e}')
#     else:
#         log.info(order_res)
#
#     return order_res
