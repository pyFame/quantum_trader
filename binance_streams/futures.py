from binance import BinanceSocketManager

from conf import async_client
from enums import Symbol


class Futures():

    @staticmethod
    async def kline_socket(symbol: Symbol, interval="1m"):
        bm = BinanceSocketManager(async_client)

        async with bm.kline_futures_socket(symbol=Symbol, interval=interval) as stream:
            while True:
                res = await stream.recv()
                print(res)
