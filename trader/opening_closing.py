from queue import Queue

from conf import alog
from utils import Futures, account
from utils.thread import keepAlive

from conf.log import *

closes = Queue(100)
opens = Queue(100)


@keepAlive
def opening():
    while 1:
        n, pos = opens.get()
        try:
            x = n.compute()
            # if pos.max_profit>0: closes.put([pos.close(price=pos.max_profit),pos])   #can cause losses in case...
            alog.info(x)
        except Exception as e:
            if hasattr(e, 'code'):
                alog.error(f"@open {e.code} {e.message}")
                over_flow = [-2027, -2019, -4164]  # max lev,margin insufficient,order notional
                if e.code in over_flow and pos.quantity > 0: pos.disable_open = False
            else:
                alog.exception('@open')


@keepAlive
def closing():
    while 1:
        n, pos = closes.get()
        try:
            x = n.compute()
            alog.info(x)
            Futures.transfer_to('SPOT', amt=.6 * pos.profit)  # babylonian
        except Exception as e:
            # alog.exception("@close")
            if hasattr(e, 'code'):
                alog.error(f"@close {e.code} {e.message}")
                if e.code == -4045:
                    account.cancel_order(pos.coin)  # max stop Order  #-2021 would immediately trigger
            else:
                log.exception('@close')
        else:
            ic('Sell Successfull')
            pos.disable_open = True
