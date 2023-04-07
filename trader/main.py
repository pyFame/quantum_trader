from icecream import ic

from enums import Symbol
from enums.position import SHORT
from trader.Position import Position


def main():
    symbol = Symbol("BTC")

    position = Position(symbol, SHORT, 1)
    ic(position)


if __name__ == "__main__":
    main()
