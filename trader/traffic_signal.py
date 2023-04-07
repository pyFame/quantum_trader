from utils.thread import keepAlive


class SignalHandler():
    @keepAlive
    def buying(self):
        short = self.SHORT
        long = self.LONG
        while 1:
            p = self.buys.get()
            if short.sell_signal(p): closes.put([short.close(p), short])

            if long.disable_open:
                if short.quantity > 0 and short.entry_price < p: continue
                opens.put([long.open(self.AMOUNT, p), long])

    @keepAlive
    def selling(self):
        short = self.SHORT
        long = self.LONG
        while 1:
            s = self.sells.get()
            if long.sell_signal(s):
                closes.put([long.close(s), long])

            if short.disable_open:
                if long.quantity > 0 and long.entry_price > s: continue
                opens.put([short.open(self.AMOUNT, s), short])
