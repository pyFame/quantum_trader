import json
import time
from datetime import timedelta

import datetime as dt

from icecream import ic

from lib.kafka import Kafka, KafkaMessage

from order import *
from macd import Macd_Strategy
from utils import Time, Pandas
from utils.Futures import Futures

from enums import Symbol


def main():
    symbol: Symbol = Symbol('BTC')
    interval: str = '1m'
    timeout: float = 1
    AMOUNT: float = .01

    df = Futures.History(symbol, interval, "4 hour ago", "1 min ago")

    ic(df.tail(1))

    macd_1 = Macd_Strategy(df, 12, 26, 9)

    k = Kafka()
    k.producer()
    topic = "futures_orders"

    while True:
        last_updated = Pandas.latest_time(df)

        df_1 = Futures.History(symbol, interval, last_updated)

        df.drop(last_updated, inplace=True)

        df = df.combine_first(df_1)

        macd_1.update(df)

        df_high = df['high'].iloc[-1]
        df_low = df['low'].iloc[-1]

        o: Order = None

        if macd_1.buy_signal():

            # o = Order(symbol,OPEN,LONG,AMOUNT,trail=0.5)
            # o = Order(symbol,OPEN,LONG,AMOUNT)
            o = Order(symbol, CLOSE, SHORT, AMOUNT, profit=df_low)  # ,trail=0.1)

            macd_1.buy()

        elif macd_1.sell_signal():

            # o = Order(symbol,CLOSE,LONG,AMOUNT,trail=0.5)
            # o = Order(symbol,CLOSE,LONG,AMOUNT,profit=df_high)

            o = Order(symbol, OPEN, SHORT, AMOUNT, profit=df_high)

            macd_1.sell()

        if o is not None:
            now_: dt.datetime = Time.now(timedelta())

            key = f"{symbol}"

            expired_at = now_ + timedelta(seconds=timeout)

            ic(o)

            val = {
                "order": o.binance_order,
                "created_at": now_.timestamp(),
                "expired_at": expired_at.timestamp(),
                "created": str(now_),
                "expired": str(now_),
            }

            msg = KafkaMessage(topic, key, json.dumps(val))
            ic(msg)
            k.publish(msg)

        time.sleep(timeout)


if __name__ == "__main__":
    main()
