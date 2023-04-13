from typing import Final

from conf.kafka import TOPIC_SIGNALS
from lib.kafka import Kafka, ConsumerProperties, LATEST
from trader import alog
from trader.consume_signals import consume_signal
from trader.publish_orders import handle_delayed_orders


def main():
    alog.info("starting microservice- trader")

    CG_ID: Final[str] = "trader"
    POLLING_TIMEOUT = 1.0  # FIXME

    handle_delayed_orders()

    kafka_client = Kafka("conf/kafka.txt")

    while True:
        consumer_ppt = ConsumerProperties(TOPIC_SIGNALS, CG_ID, LATEST, callback=consume_signal,
                                          poll_timeout=POLLING_TIMEOUT)
        consumer = kafka_client.consumer(consumer_ppt)
        consumer.consume()


if __name__ == "__main__":
    main()
