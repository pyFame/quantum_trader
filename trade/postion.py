class Position():
    q, c = 0, 0  # c is entry price, qis quantity
    flag = True

    def __init__(self, mode, crypto, profit, hedge=True, open_args={}, close_args={},
                 trend=math.inf):  # basically take 0-long
        self.pos = 'SHORT' if mode == 'S' else 'LONG'
        self.profit = profit
        self.crypto = crypto
        self.PRECISION = precision(crypto)
        self.hedge = hedge
        self.open_args = open_args
        self.close_args = close_args
        self.trend = 1
        self.refresh()

    def __call__(self):
        print(self.status())

    def status(self):
        return self.q, self.c, self.pos

    def __repr__(self):
        return f'{self.status()}'

    @property
    def cost(self):
        return self.c * self.q if self.q > 0 else 0

    def pnl(self, p, q=0):
        q = q if q else self.q
        net = (p - self.c) * q
        if self.pos == 'SHORT': return -net
        return net

    @delayed
    def open(self, q, p=''):
        if not (self.hedge and self.flag): return f"{self.crypto} {self.pos} disabled"
        d = self.open_args
        d['quantity'] = q
        paras = ['price', 'profit', 'loss']
        for i in paras:
            if i in d: d[i] = d[i] or p
        x = order(self.crypto, 'OPEN', self.pos, **d)
        self.refresh()
        return x

    @delayed
    def close(self, p='', q='', **args):
        d = self.close_args
        d.update(args)
        d['quantity'] = q or self.q
        if p:
            paras = ['price', 'profit', 'loss']
            for i in paras:
                if i in d: d[i] = p
        x = order(self.crypto, 'CLOSE', self.pos, **d)
        self.refresh()
        return x

    @keepAlive
    def refresh(self):
        data = positions(self.crypto, self.pos)
        self.q, self.c = pluck_row(data, 'positionAmt', 'entryPrice')

    def sell_signal(self, p, q=''):
        return self.pnl(p, q) >= self.profit

    @property
    def liqPrice(self):
        data = positions(self.crypto, self.pos)
        liq = pluck_row(data, 'liquidationPrice')
        return liq

    @property
    def max_profit(self):
        if self.q > 0:
            p = (self.profit * 2) / self.q
            p = self.c - p if self.pos == 'SHORT' else self.c + p
        else:
            return 0
        return p
