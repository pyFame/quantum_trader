from dask import compute, delayed

from order_consumer.main import main as main_order_consumer
from strategy.main import main as main_start_strategy
from utils.thread import undead


@delayed
def start_strategy():
    main_start_strategy()


@delayed
def start_order_consumer():
    main_order_consumer()


def main():
    compute([
        start_strategy(),
        start_order_consumer(),
    ], scheduler="processes")


if __name__ == "__main__":
    main()
