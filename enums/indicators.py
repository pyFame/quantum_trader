from typing import Final, Union, List
from dataclasses import dataclass

MACD: Final[str] = "MACD"
RSI: Final[str] = "RSI"
BUY: Final[str] = "BUY"
SELL: Final[str] = "SELL"


@dataclass
class Message_Signal:
    indicator: Union[MACD, RSI]
    signal: Union[BUY, SELL]

    low: float = None  # FIXME later mandate it...
    high: float = None

    indicator_value: float = None
    filters: List[dict] = None  # {"SMA",200}
