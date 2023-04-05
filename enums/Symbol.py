
from dataclasses import dataclass

from typing import Type
import json

@dataclass(frozen=True)
class Symbol(str):
    base: str
    quote: str = "USDT"

    def __post_init__(self):
        if len(self.base) < 3 or len(self.base) >= 5:
            raise ValueError(f"Invalid Base Coin-{self.base}")

    def __new__(cls, base: str, quote: str = "USDT") -> str:
        return super().__new__(cls, f"{base.upper()}{quote.upper()}")

    def __repr__(self) -> str:
        return self.__str__() #f"Symbol('{self.base}', '{self.quote}')"

    def __str__(self) -> str:
        return f"{self.base}{self.quote}"

    def dumps(self)->str:
        return json.dumps(f"{self.base}/{self.quote}")

    @staticmethod    
    def loads(json_dump:str)->'Symbol':
        symbol_str:str = json.loads(json_dump)
        return Symbol(*symbol_str.split('/'))

    @staticmethod
    def Parse(symbol_str:str)->'Symbol':
      return Symbol.loads(json.dumps(symbol_str))
