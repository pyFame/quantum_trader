from dataclasses import dataclass
import math
from typing import Union, Optional

import pandas as pd
from icecream import ic

from enums import Symbol
from enums.position import SHORT, LONG
from utils import Futures
from utils.Pandas import pluck_row
from utils.thread import keepAlive


@dataclass
class Position:
    mode: Union[LONG, SHORT]
    symbol: Symbol

    profit: float
    hedge: Optional[bool] = True  # Do SHORT,LONG Simultaneously

    _precision = Futures.precision(symbol)

    open_args: Optional[dict] = None
    self_args: Optional[dict] = None

    flag = True
    q, c = 0, 0  # c is entry price, qis quantity

    def __post_init__(self):
        symbol = self.symbol
        self.coin = symbol.base

        self.open_args = self.open_args or {}
        self.close_args = self.close_args or {}

        self.refresh()

    def __call__(self):
        print(self.status())

    def status(self):
        return self.q, self.c, self.pos

    def __repr__(self):
        return f'{self.status()}'

    @property
    def cost(self) -> float:
        return self.c * self.q

    def pnl(self, price: float, quantity: float = 0) -> float:
        quantity = quantity if quantity else self.q
        net = (price - self.c) * quantity
        if self.pos == SHORT: return -net
        return net

    # @delayed
    def open(self, q, p=''):  # TODO
        if not (self.hedge and self.flag):
            ic(f"{self.coin} {self.pos} disabled")
            return
        d = self.open_args
        d['quantity'] = q
        paras = ['price', 'profit', 'loss']
        for i in paras:
            if i in d: d[i] = d[i] or p
        # x = order(self.coin, 'OPEN', self.pos, **d)
        # self.refresh()
        return

    # @delayed
    def close(self, p='', q='', **args):  # TODO
        d = self.close_args
        d.update(args)
        d['quantity'] = q or self.q
        if p:
            paras = ['price', 'profit', 'loss']
            for i in paras:
                if i in d: d[i] = p
        # x = order(self.coin, 'CLOSE', self.pos, **d)
        # self.refresh()
        return

    @keepAlive
    def refresh(self):
        data = Futures.current_positions(self.symbol, self.mode)
        self.q, self.c = pluck_row(data, 'positionAmt', 'entryPrice')

    def sell_signal(self, p, q='') -> bool:
        return self.pnl(p, q) > self.profit

    @property
    def liqPrice(self) -> float:
        data = Futures.current_positions(self.symbol, self.mode)
        liq = pluck_row(data, 'liquidationPrice')
        return liq

    @property
    def max_profit(self) -> float:
        p = 0
        if self.q > 0:
            p = (self.profit * 2) / self.q
            p = self.c - p if self.mode == SHORT else self.c + p

        return p
