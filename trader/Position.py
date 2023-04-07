from dataclasses import dataclass
from typing import Union, Optional

from icecream import ic

from conf import alog
from enums import Symbol
from enums.position import SHORT, LONG
from trader.order import Order, OPEN, CLOSE
from utils import Futures
from utils.Pandas import pluck_row
from utils.thread import keepAlive


@dataclass
class Position:
    symbol: Symbol
    mode: Union[LONG, SHORT]

    profit: float
    # hedge: Optional[bool] = True  # Do SHORT,LONG Simultaneously

    open_args: Optional[dict] = None
    close_args: Optional[dict] = None

    disable_open = False
    quantity, entry_price = 0, 0  # c is entry price, q is quantity

    def __post_init__(self):
        symbol = self.symbol
        self.coin = symbol.base

        self.open_args = self.open_args or {}
        self.close_args = self.close_args or {}

        self.refresh()

    def pnl(self, price: float, quantity: float = 0) -> float:
        quantity = quantity or self.quantity
        net = (price - self.entry_price) * quantity
        if self.mode == SHORT:
            net = -1 * net
        return net

    def open(self, quantity: float, price=None) -> Order:
        if self.disable_open:
            ic(f"{self.symbol} {self.mode} disabled")
            return
        d = self.open_args

        d["side"] = OPEN
        d["mode"] = self.mode
        d['quantity'] = quantity

        prices_args = ['price', 'profit', 'loss']
        for i in prices_args:
            if i in d:
                d[i] = d[i] or price

        o = Order(**d)
        alog.debug(o)

        return o

    def close(self, price: float = None, quantity: float = None, **args) -> Order:
        d = self.close_args
        d.update(args)

        d["side"] = CLOSE
        d["mode"] = self.mode
        d['quantity'] = quantity or self.quantity

        if price:
            prices_args = ['price', 'profit', 'loss']
            for i in prices_args:
                if i in d:
                    d[i] = d[i] or price
        o = Order(**d)
        alog.debug(o)

        return o

    def sell_signal(self, p, q=None) -> bool:
        return self.pnl(p, q) > self.cost  # FIXME self.profit

    @property
    def liquidation_price(self) -> float:
        data = Futures.current_positions(self.symbol, self.mode)
        liq = pluck_row(data, 'liquidationPrice')
        return liq

    @property
    def ideal_price(self) -> float:
        p = 0.
        if self.quantity > 0:
            p = (self.profit * 2) / self.quantity
            p = self.entry_price - p if self.mode == SHORT else self.entry_price + p

        return p

    @property
    def cost(self) -> float:
        return self.entry_price * self.quantity

    @property
    def precision(self):
        return Futures.precision(self.symbol, cache=True)

    @keepAlive
    def refresh(self):
        data = Futures.current_positions(self.symbol, self.mode)
        self.quantity, self.entry_price = pluck_row(data, 'positionAmt', 'entryPrice')

    def __call__(self):
        print(self.status())

    def status(self):
        return self.quantity, self.entry_price, self.mode

    def __repr__(self):
        return f'{self.status()}'
