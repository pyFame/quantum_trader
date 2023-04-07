from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from typing import Union, Set, Tuple, List

import pandas as pd


@dataclass
class Strategy(ABC):
    # closes : Union[np.ndarray,List,Tuple,pd.Series]
    ohlcv: pd.DataFrame

    name: str = field(init=False)

    price: float = field(init=False, default=0.)

    signal: int = field(init=False, default=-1)

    # price,signal = 0.,-1

    @abstractmethod
    def __post_init__():
        # print("abstract")
        pass

    @abstractmethod
    def buy_signal(self) -> bool:
        pass

    @abstractmethod
    def sell_signal(self) -> bool:
        pass

    def update(self, ohlcv: pd.DataFrame):
        self.ohlcv = ohlcv
        self.__post_init__()

    def buy(self, price: float = 0.):
        self.signal = 0
        self.price = price

    def sell(self, price: float = 0.):
        self.signal = 1
        self.price = price

    def __repr__(self):
        return f"{self.name}"

    @property
    def closes(self) -> pd.Series:
        return self.ohlcv["close"]

    @property
    def last_close(self) -> float:
        return self.closes.iloc[-1]
