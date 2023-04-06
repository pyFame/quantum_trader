from lib.kafka import Kafka, ConsumerProperties, LATEST
from config_kafka import CG_ID, TOPIC, POLLING_TIMEOUT
from order_computing import order_computing, callback


def main():
    order_computing()  # daemon thread

    k = Kafka()

    consumer_ppt = ConsumerProperties(TOPIC, CG_ID, LATEST, POLLING_TIMEOUT, callback)

    consumer = k.consumer(consumer_ppt)
    consumer.consume()


if __name__ == "__main__":
    # log.info("hey") #causing error when
    main()
