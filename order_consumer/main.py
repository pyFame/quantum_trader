from conf import alog
from conf.kafka import TOPIC_ORDERS
from lib.kafka import Kafka, ConsumerProperties, LATEST
from order_consumer.config_kafka import CG_ID, POLLING_TIMEOUT
from order_consumer.order_computing import order_computing, callback


def main():
    alog.info("starting microservice- order_consumer")
    order_computing()  # daemon thread

    k = Kafka()

    consumer_ppt = ConsumerProperties(TOPIC_ORDERS, CG_ID, LATEST, POLLING_TIMEOUT, callback)

    consumer = k.consumer(consumer_ppt)
    consumer.consume()


if __name__ == "__main__":
    main()
