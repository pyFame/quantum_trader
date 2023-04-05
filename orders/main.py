from kafka import Kafka, ConsumerProperties, LATEST
from orders.config import cg_id
from orders.order_computing import order_computing, callback


def main():
    order_computing()  # daemon thread

    POLLING_TIMEOUT = 1.0

    k = Kafka()

    consumer_ppt = ConsumerProperties("futures_orders", cg_id, LATEST, POLLING_TIMEOUT, callback)

    consumer = k.consumer(consumer_ppt)
    consumer.consume()


if __name__ == "__main__":
    main()
