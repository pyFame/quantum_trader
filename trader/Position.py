from dataclasses import dataclass
from typing import Union, Optional

from icecream import ic

from enums import Symbol
from enums.Order import Order, OPEN, CLOSE
from enums.position import SHORT, LONG
from trader import alog
from utils import Futures
from utils.Pandas import pluck_row


@dataclass
class Position:
    symbol: Symbol
    mode: Union[LONG, SHORT]

    profit: float = 1  # remove its meant to be more than 1 dollar
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

        self.open_args |= {"symbol": symbol}  # FIXME compatibility with python3.9
        self.close_args |= {"symbol": symbol}

        self.refresh()

    def pnl(self, price: float, quantity: float = 0) -> float:
        quantity = quantity or self.quantity
        net = (price - self.entry_price) * quantity
        if self.mode == SHORT:
            net = -1 * net
        return net

    def open(self, quantity: float, price: float = None) -> Order:
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

    def close(self, quantity: float = None, price: float = None, **args) -> Order:
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

    def open_signal(self, p: float) -> bool:
        if self.disable_open: return False

        if self.quantity > 0:
            if self.mode is LONG:
                return p < self.entry_price

            if self.mode is SHORT:
                return p > self.entry_price

        return True

    def close_signal(self, p: float, q: float = None) -> bool:
        if self.quantity <= 0: return False

        return self.pnl(p, q) > 0  # > self.cost  # FIXME self.profit

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

    def refresh(self):
        data = Futures.current_positions(self.symbol, self.mode)
        self.quantity, self.entry_price = pluck_row(data, 'positionAmt', 'entryPrice')

    def __call__(self):
        print(self.status())

    def status(self):
        return self.quantity, self.entry_price, self.mode

    def __repr__(self):
        return f'{self.status()}'
