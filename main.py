from dask import compute

from order_consumer.main import main as start_order_consumer
from strategy.main import main as start_strategy
from utils.thread import undead


def main():
    compute(*[
        start_strategy(),
        start_order_consumer(),
    ], scheduler="processes")


if __name__ == "__main__":
    main()
