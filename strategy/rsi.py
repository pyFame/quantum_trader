from dataclasses import dataclass, field
from typing import Union

import numpy as np
import pandas as pd
import talib

from .Strategy import Strategy


@dataclass
class RSI_Strategy(Strategy):
    period: int = 14
    over: int = 80
    under: int = 20

    name: str = field(init=False, default="RSI")
    # boughtAlready: int = 0
    # soldAlready: int = 0
    rsis: pd.Series = field(init=False)
    cur_rsi: float = field(init=False)  # l

    def __post_init__(self):
        # super(self.name,self.ohlcv) #not required
        closes = self.closes

        if len(closes) < self.period:
            print('invalid closes')
            return

        rsi = self.Rsi(closes, self.period)

        self.rsis = rsi

    @property
    def cur_rsi(self):
        return self.rsis.iloc[-1]

    @staticmethod
    def Rsi(closes: Union[np.ndarray, pd.Series], period: int = 14):
        return talib.RSI(closes, period)

    def buy_signal(self, under) -> bool:
        cur_rsi = self.cur_rsi
        signal = self.signal
        under = under or self.under

        buy_signal = cur_rsi <= under and signal != 0
        if buy_signal:
            alog.debug("OverSold")

        return buy_signal

    def sell_signal(self, over) -> bool:
        cur_rsi = self.cur_rsi
        over = over or self.over
        signal = self.signal

        sell_signal = cur_rsi >= over and signal != 1

        if sell_signal:
            alog.debug("OverBought")

        return sell_signal
