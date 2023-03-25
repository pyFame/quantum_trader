class Socket():
    async def trade_socket(self, type='F'):
        crypto = self.SYMBOL
        if type == 'F':
            conn = socket.aggtrade_futures_socket(crypto)
        elif type == 'S':
            conn = socket.trade_socket(crypto)
        elif type == 'SA':
            conn = socket.aggtrade_socket(crypto)
        return conns

    async def kline_socket(self, interval='1m', type='F'):
        d = {'symbol': self.SYMBOL, 'interval': interval}
        if type == 'S': return socket.kline_socket(**d)
        return socket.kline_futures_socket(**d)

    async def market_socket(self):
        return socket.symbol_mark_price_socket(self.SYMBOL)


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