from binance import BinanceSocketManager
from  unsync import unsync
class Socket():
    @unsync
    async def socket_manager(client):
        # c1 = await AsyncClient.create() if not client else client
        self.socket = BinanceSocketManager(client)
        return self.socket
    async def trade_socket(self, type='F'):
        coin = self.SYMBOL
        if type == 'F':
            conn = self.socket.aggtrade_futures_socket(coin)
        elif type == 'S':
            conn = self.socket.trade_socket(coin)
        elif type == 'SA':
            conn = self.socket.aggtrade_socket(coin)
        return conns

    async def market_socket(self):
        return self.socket.symbol_mark_price_socket(self.SYMBOL)


class SocketHandler():
    async def handle_socket(self, msg):
        d = msg['data']
        S, T, p = pluck(d, 's', 'E', 'p')
        p = float(p)
        self.CLOSES = np.append(self.CLOSES, p)
        self.MACDStrategy(p, 12, 26, 9)

    async def socket_handler(self, conn, handler, y):
        async with conn as SM:
            i = 0
            while i < y:
                try:
                    res = await SM.recv()
                except:
                    log.debug('Already SM')
                else:
                    await handler(res)
                i += 1
                # asyncio.sleep(1)
            # await ts.__aenter__().
            # await ts.__aexit__(None, None, None)