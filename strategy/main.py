from enums import Symbol
from utils.Futures import Futures

symbol: Symbol = Symbol('EOS')
interval: str = '1m'
timeout: float = 1
AMOUNT: float = 5

df = Futures.History(symbol, interval, "4 hour ago", "1 min ago")

df.tail(1)
