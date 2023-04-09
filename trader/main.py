from icecream import ic

from enums import Symbol
from enums.indicators import MACD, RSI
from enums.position import SHORT
from lib.kafka import Kafka, ConsumerProperties, LATEST
from trader.config_kafka import SIGNAL_TOPIC, CG_ID, POLLING_TIMEOUT
from trader.Position import Position

indicators = {
    MACD: 1,  # priority stuffs
    RSI: .1
}


def main():
    symbol = Symbol("BTC")

    position = Position(symbol, SHORT, 1)
    ic(position)

    while True:  # msg: BUY:  val: symbol: BTC/USDT indicator: MACD
        k = Kafka()
        consumer_ppt = ConsumerProperties(SIGNAL_TOPIC, CG_ID, LATEST, POLLING_TIMEOUT, callback)

        consumer = k.consumer(consumer_ppt)
        consumer.consume()


if __name__ == "__main__":
    main()
