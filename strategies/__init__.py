class Strategy():
    rsi_q = Queue(100)
    macd_q = Queue(100)

    def RSIStrategy(self, price, period=14):

        if self.CLOSES.size <= period: return

        rsi = talib.RSI(self.CLOSES, period)
        cur_rsi = rsi[-1]

        self.rsi_q.put((price, cur_rsi))

    @keepAlive
    def rsing(self):
        under, over = 20, 80
        signal = -1
        while 1:
            price, cur_rsi = self.rsi_q.get()
            if cur_rsi <= under and signal != 0:
                ic("OverSold")
                self.buys.put(price)
                signal = 0
            elif cur_rsi >= over and signal != 1:
                ic("OverBought")
                self.sells.put(price)
                signal = 1

    def cur_macd(self, prices, fast, slow, signal):  # talib is faster ...
        macds = talib.MACD(prices, fastperiod=fast, slowperiod=slow, signalperiod=signal)  # macd,signal,histogram
        m, s, h = [macds[i][-1] for i in range(3)]
        return m, s

    def MACDStrategy(self, price, fast=12, slow=26, signal=9):  # CLOSES must be updated..
        macd, signal = self.cur_macd(self.CLOSES, fast, slow, signal)
        self.macd_q.put((price, macd, signal))

    @keepAlive
    def macding(self):
        signal = 0  # change quantity according to signal averaging method but avoid for now
        while 1:
            data = self.macd_q.get()
            ic(f"MACD {data}")
            p, m, s = data  # pluck(data,'price','macd','signal')
            if m > s:
                if signal != 1:
                    self.buys.put(p)
                    signal = 1
            elif m < s:
                if signal != -1:
                    self.sells.put(p)
                    signal = -1