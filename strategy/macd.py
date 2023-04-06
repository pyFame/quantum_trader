from dataclasses import field, dataclass
from typing import Union

import numpy as np
import pandas as pd
import talib
from icecream import ic

from strategy import Strategy


@dataclass
class Macd_Strategy(Strategy):
    fast_period: int = 12
    slow_period: int = 26
    signal_period: int = 9

    name: str = field(init=False, default="MACD")

    # macd_tup: Tuple[pd.Series, pd.Series, pd.Series] = field(init=False)

    macd: pd.DataFrame = field(init=False)

    def __post_init__(self):
        closes = self.closes

        # if len(closes) < self.slow_period:
        #   print('invalid closes')
        # return
        macd_df = self.Macd(closes, self.fast_period, self.slow_period, self.signal_period)

        self.macd = macd_df

    @staticmethod
    def Macd(prices: Union[pd.Series, np.ndarray], fast_period=12, slow_period=26, signal_period=9) -> pd.DataFrame:
        macd, macdsignal, macdhist = talib.MACD(prices, fast_period, slow_period, signal_period)

        macd_dict = {'macd': macd, 'signal': macdsignal, 'hist': macdhist}

        macd_df = pd.DataFrame(macd_dict)

        return macd_df

    @property
    def cur_macd(self):
        # m, s, h = [macds_tup[i][-1] for i in range(3)] #optimised version
        return self.macd.iloc[-1]

    def buy_signal(self) -> bool:
        m, s, h = self.cur_macd
        signal = self.signal

        # Check if MACD crosses above signal line and is above zero
        buy_signal = m > s  # not sure there is more to it and m > 0

        if buy_signal and signal != 0:
            ic("Buy signal")

            closes = self.closes.values

            # Add a trend filter (200-day SMA)
            sma_200 = talib.SMA(closes, timeperiod=200)
            if closes[-1] > sma_200[-1]:
                ic("Trend is up")
                # Add a momentum filter (RSI)
                rsi = talib.RSI(closes, timeperiod=14)
                if rsi[-1] > 50:
                    ic("Momentum is strong")
                    return True

        return False

    def sell_signal(self) -> bool:
        m, s, h = self.cur_macd
        signal = self.signal

        sell_signal = m < s  # m<0

        # Check if MACD is below zero
        if sell_signal and signal != 1:
            ic("Sell signal")

            closes = self.closes.values  # np.array

            # Add a trend filter (200-day SMA)
            sma_200 = talib.SMA(closes, timeperiod=200)
            if closes[-1] < sma_200[-1]:
                ic("Trend is down")

                # Add a momentum filter (RSI)
                rsi = talib.RSI(closes, timeperiod=14)
                if rsi[-1] < 50:
                    ic("Momentum is weak")
                    return True

        return False
