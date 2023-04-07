import websockets
import logging as log

import asyncio

from enums import *


class Socket():
    from typing import Callable, Awaitable

    def __init__(self, symbol: str, socket_type: str):

        self.symbol = symbol
        self.socket_type = socket_type
        self.socket = self.futures_socket_gen(symbol, socket_type)

        return

    @staticmethod
    async def handle_socket_message(msg):
        print(msg)

    @staticmethod
    def futures_socket_gen(symbol: str, socket_type: str):
        from binance import BinanceSocketManager

        bm = BinanceSocketManager(async_client)

        sockets = {
            FUTURES_DEPTH: bm.futures_depth_socket,
            FUTURES_AGG: bm.aggtrade_futures_socket,
            FUTURES_KLINE: bm.kline_futures_socket,
        }

        # Set up the binance_streams based on the binance_streams type
        socket = sockets.get(socket_type, None)

        if socket == None: raise ValueError("Invalid binance_streams type")

        return socket(symbol)

    @staticmethod
    async def start_socket(socket, *socket_handlers: Callable[[str], Awaitable[None]]):
        RETRY_INTERVAL = 20
        TIMEOUT = 60 * 5  # FIXME: change

        while True:
            try:
                async with socket as stream:
                    while True:
                        msg = await asyncio.wait_for(stream.recv(), timeout=TIMEOUT)
                        await asyncio.gather(*[handle_socket_message(msg) for handle_socket_message in socket_handlers])

            except websockets.exceptions.ConnectionClosed:
                log.info(f"Websocket disconnected. Retrying in {RETRY_INTERVAL} seconds.")
                await asyncio.sleep(RETRY_INTERVAL)
            except Exception as e:
                log.exception(f"Exception in start_socket: {e}")
                await asyncio.sleep(1)

    async def start(self, *socket_handlers: Callable[[str], None]):
        socket_handlers = self.handle_socket_message if len(socket_handlers) == 0 else socket_handlers
        return await self.start_socket(self.socket, socket_handlers)
