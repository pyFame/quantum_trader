from dask import compute, delayed

from order_consumer.main import main as main_order_consumer
from strategy.main import main as main_start_strategy
from trader.main import main as main_trader


@delayed
def start_strategy():
    main_start_strategy()


@delayed
def start_order_consumer():
    main_order_consumer()


@delayed
def start_trader():
    main_trader()


def main():
    compute(*[
        start_strategy(),
        start_order_consumer(),
        start_trader,
    ], scheduler="threads")  # FIXME make it processes after implementing logger that is process safe


if __name__ == "__main__":
    main()
