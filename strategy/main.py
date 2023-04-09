import json
import time
from datetime import timedelta

import datetime as dt

from icecream import ic

from conf import alog
from conf.kafka import TOPIC_ORDERS
from lib.kafka import Kafka, KafkaMessage

from strategy.order import *
from strategy.macd import Macd_Strategy

from utils import Time, Pandas, Futures
from enums import Symbol


def main():
    alog.info("starting microservice-strategy")

    symbol: Symbol = Symbol('BTC')
    interval: str = '1m'
    timeout: float = 1
    AMOUNT: float = .01

    df = Futures.history(symbol, interval, "4 hour ago", "1 min ago")

    ic(df.tail(1))

    macd_1 = Macd_Strategy(df, 12, 26, 9)

    k = Kafka().producer()

    while True:
        last_updated = Pandas.latest_time(df)

        df_1 = Futures.history(symbol, interval, last_updated)

        df.drop(last_updated, inplace=True)

        df = df.combine_first(df_1)

        macd_1.update(df)

        df_high = df['high'].iloc[-1]
        df_low = df['low'].iloc[-1]

        signal = None

        if macd_1.buy_signal():
            signal = BUY
        elif macd_1.sell_signal():
            signal = SELL

        if signal is not None:
            key = symbol.json
            val = {
                "symbol": symbol.json,
                "signal": signal,
                "low": df_low,
                "high": df_high,
            }

        if o is not None:
            now_: dt.datetime = Time.now(timedelta())

            key = symbol

            expired_at = now_ + timedelta(seconds=timeout)

            ic(o)

            val = {
                "order": o.binance_order,
                "created_at": now_.timestamp(),
                "expired_at": expired_at.timestamp(),
                "created": str(now_),
                "expired": str(now_),
            }

        msg = KafkaMessage(TOPIC_ORDERS, key, json.dumps(val))
        ic(msg)
        k.publish(msg)

        time.sleep(timeout)


if __name__ == "__main__":
    main()
