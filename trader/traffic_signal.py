from utils import keepAlive


class SignalHandler():

    @keepAlive
    def buying(self):
        short = self.SHORT
        long = self.LONG
        while 1:
            p = self.buys.get()
            if short.sell_signal(p): closes.put([short.close(p), short])

            if long.flag:
                if short.q > 0 and short.c < p: continue
                opens.put([long.open(self.AMOUNT, p), long])

    @keepAlive
    def selling(self):
        short = self.SHORT
        long = self.LONG
        while 1:
            s = self.sells.get()
            if long.sell_signal(s):
                closes.put([long.close(s), long])

            if short.flag:
                if long.q > 0 and long.c > s: continue
                opens.put([short.open(self.AMOUNT, s), short])
