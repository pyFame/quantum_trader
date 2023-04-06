import logging as log

from lib.kafka import Kafka, ConsumerProperties, LATEST
from lib.kafka.enums import ConsumerProperties

from order_consumer.config import cg_id
from order_consumer.order_computing import order_computing, callback

from icecream import ic


def main():
    order_computing()  # daemon thread

    POLLING_TIMEOUT = 1.0

    k = Kafka()

    consumer_ppt = ConsumerProperties("futures_orders", cg_id, LATEST, POLLING_TIMEOUT, callback)

    consumer = k.consumer(consumer_ppt)
    consumer.consume()


if __name__ == "__main__":
    log.info("hey")
    # main()
