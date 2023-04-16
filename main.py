from order_consumer.main import main as main_order_consumer
from strategy.main import main as main_start_strategy
from trader.main import main as main_trader
from utils.thread import keepAlive


@keepAlive(daemon=False)
def start_strategy():
    main_start_strategy()


# @keepAlive(daemon=False)
def start_order_consumer():
    main_order_consumer()


# @undead
@keepAlive(daemon=False)
def start_trader():
    main_trader()


def main():
    start_strategy()
    start_trader()
    start_order_consumer()
    # time.sleep()

    # compute(*[
    #     start_strategy(),
    #     start_order_consumer(),
    #     start_trader(),
    # ], scheduler="threads")  # FIXME make root logger safe


if __name__ == "__main__":
    main()
