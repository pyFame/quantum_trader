async def kline_socket(self, interval='1m', type='F'):
    d = {'symbol': self.SYMBOL, 'interval': interval}
    if type == 'S': return socket.kline_socket(**d)
    return socket.kline_futures_socket(**d)