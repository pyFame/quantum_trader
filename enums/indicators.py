import json
from dataclasses import dataclass
from datetime import datetime
from typing import Final, Union, List

from utils import Time, Dataclass

MACD: Final[str] = "MACD"
RSI: Final[str] = "RSI"
BUY: Final[str] = "BUY"
SELL: Final[str] = "SELL"


@dataclass(slots=True)
class Message_Signal(Dataclass.DataClassJson):
    indicator: Union[MACD, RSI]
    signal: Union[BUY, SELL]

    low: float = None  # FIXME later mandate it...
    high: float = None

    indicator_value: float = None
    filters: List[dict] = None  # {"SMA",200}

    created_at: float = None  # field(init=False, default=None)
    created: str = None  # field(init=False, default=None)

    def __post_init__(self):
        if self.created_at is None:
            now_: datetime = Time.now_utc()
            self.created_at = now_.timestamp()
            self.created = str(now_)

    @staticmethod
    def Loads(json_str: str) -> 'Message_Signal':
        args = json.loads(json_str)
        return Message_Signal(**args)
