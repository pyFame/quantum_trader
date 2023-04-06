import pytest

from enums import Symbol
from strategy.order import *

import logging as log


# @pytest.mark.no_cache
# @pytest.mark.parametrize("i", range(50))
def test_order():
    log.basicConfig(filename='test.log', level=log.INFO)
    log.info("Starting test...")

    symbol = Symbol("EOS")
    AMOUNT: float = 5

    o = Order(symbol, CLOSE, SHORT, AMOUNT, profit=2)

    expected_res = {
        "type": "TAKE_PROFIT_MARKET",
        "symbol": symbol,
        "quantity": AMOUNT,
        "positionSide": SHORT,
        "side": "SELL",
        "priceProtect": True,
        "stopPrice": o.profit
    }
    assert o.d == expected_res
