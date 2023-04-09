import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Final, Union, List

from utils import Time, Dataclass

MACD: Final[str] = "MACD"
RSI: Final[str] = "RSI"
BUY: Final[str] = "BUY"
SELL: Final[str] = "SELL"


@dataclass
class Message_Signal(Dataclass.DataClassJson):
    indicator: Union[MACD, RSI]
    signal: Union[BUY, SELL]

    low: float = None  # FIXME later mandate it...
    high: float = None

    indicator_value: float = None
    filters: List[dict] = None  # {"SMA",200}

    created_at: float = field(init=False, default=None)
    created: str = field(init=False, default=None)

    def __post_init__(self):
        now_: datetime = Time.now(timedelta())

        self.created_at = now_.timestamp()
        self.created = str(now_)

    @staticmethod
    def Loads(json_str: str) -> object:
        args = json.loads(json_str)
        return Message_Signal(**args)
