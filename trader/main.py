from typing import Final

from conf.kafka import TOPIC_SIGNALS
from lib.kafka import Kafka, ConsumerProperties, LATEST
from trader.consume_signals import consume_signal
from trader.publish_orders import handle_delayed_orders


def main():
    CG_ID: Final[str] = "trader"
    POLLING_TIMEOUT = 10.0  # FIXME

    handle_delayed_orders()

    kafka_client = Kafka()

    while True:
        consumer_ppt = ConsumerProperties(TOPIC_SIGNALS, CG_ID, LATEST, consume_signal, POLLING_TIMEOUT)
        consumer = kafka_client.consumer(consumer_ppt)
        consumer.consume()


if __name__ == "__main__":
    main()
