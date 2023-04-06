from dataclasses import dataclass, field
from typing import Optional, Union, Final

from enums import Symbol
from utils.Futures import Futures

BUY: Final[str] = "BUY"
SELL: Final[str] = "SELL"

OPEN: Final[str] = "OPEN"
CLOSE: Final[str] = "CLOSE"

LONG: Final[str] = "LONG"
SHORT: Final[str] = "SHORT"


@dataclass(frozen=False)  # TODO: should be true
class Order:
    symbol: Symbol
    side: Union[OPEN, CLOSE]
    mode: Union[LONG, SHORT]

    quantity: float = None
    price: float = None

    profit: float = None
    loss: float = None

    trail: float = None  # Used with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%

    protect: bool = True  # priceProtect

    d: dict = field(init=False, default=None)

    def __post_init__(self):
        self.correct_with_precision()

        d = {"type": "MARKET"}

        self.d = d

        quantity = self.quantity
        mode = self.mode

        d.update(
            {"symbol": str(self.symbol), "quantity": quantity, "positionSide": mode}
        )  # d|= merge operator

        price = self.price
        profit = self.profit
        loss = self.loss
        trail = self.trail

        if trail:
            if quantity is None: raise ValueError("qauntity required for TRAILING_STOP_MARKET")
            d["type"] = "TRAILING_STOP_MARKET"
            d["callbackRate"] = trail

            if price:
                d["activationPrice"] = price

            if profit or loss:
                raise ValueError("profit or loss not required only- supports price")
        elif price:
            d["type"] = "LIMIT"
            d["price"] = price
            d["timeInForce"] = "GTC"

        if profit:
            d["type"] = "TAKE_PROFIT" if price else "TAKE_PROFIT_MARKET"
            d["stopPrice"] = profit
            # if price is None:
            #   if profit is None:
            #     raise ValueError(f"profit/stopPrice required for {d["type"]}")
            # stop price is used to trigger the sell
        elif loss:
            d["type"] = "STOP" if price else "STOP_MARKET"
            d["stopPrice"] = loss

        if profit or loss:
            d["priceProtect"] = self.protect

        side = self.side

        if side == OPEN:
            d["side"] = "BUY" if mode == LONG else "SELL"

            if quantity is None:
                raise ValueError("invalid quantity")

        elif side == CLOSE:
            d["side"] = "SELL" if mode == SHORT else "BUY"
            if quantity is None:  # and (profit or loss): STOP_MARKET or TAKE_PROFIT_MARKET
                d["closePosition"] = True
                del d["quantity"]

    def correct_with_precision(self):  # TODO: make this a static method

        p, q, bP, qP, minP, maxP, minQ = Futures.Precision(self.symbol)

        quantity = self.quantity

        if quantity is not None:
            quantity = round(max(quantity, minQ), q)
            self.quantity = quantity

        def correct_price(price: float) -> Optional[float]:
            if price is None: return None

            price = round(price, p)
            price = min(maxP, price)
            price = max(minP, price)

            return price

        self.price = correct_price(self.price)

        self.profit = correct_price(self.profit)

        self.loss = correct_price(self.loss)

    @property
    def binance_order(self):
        return self.d

    # def __call__(self)->Union[pd.DataFrame,None]:
    #   return order(o.d)
