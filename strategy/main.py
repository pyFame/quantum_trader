import time

from icecream import ic

from conf import alog
from conf.kafka import TOPIC_SIGNALS
from enums.Order import *
from enums.indicators import Message_Signal, MACD
from lib.kafka import Kafka, KafkaMessage
from strategy.macd import Macd_Strategy
from utils import Pandas, Futures


def main():
    alog.info("starting microservice-strategy")

    indicator = MACD

    symbol: Symbol = Symbol('BTC')
    interval: str = '1m'
    TIMEOUT: float = 1
    AMOUNT: float = .01

    df = Futures.history(symbol, interval, "4 hour ago", "1 min ago")

    ic(df.tail(1))

    macd_1 = Macd_Strategy(df, 12, 26, 9)

    kafka_client = Kafka().producer()

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

            signal_msg = Message_Signal(indicator, signal, low=df_low, high=df_high)  # filters=[{"SMA", 200}])

            msg = KafkaMessage(TOPIC_SIGNALS, key, signal_msg.json)
            ic(msg)

            kafka_client.publish(msg)  # TODO add a callback

        time.sleep(TIMEOUT)


if __name__ == "__main__":
    main()
