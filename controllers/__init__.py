from queue import Queue

from utils.concurrency import keepAlive

from conf.setup_log import *

closes = Queue(100)
opens = Queue(100)

@keepAlive
def opening(): 
  while 1:
      n,pos = opens.get()
      try:  
          x = n.compute()
          # if pos.max_profit>0: closes.put([pos.close(price=pos.max_profit),pos])   #can cause losses in case...
          bLog.info(x)
      except Exception as e:
        if hasattr(e,'code'):
          bLog.error(f"@open {e.code} {e.message}")
          over_flow = [-2027,-2019,-4164] #max lev,margin insufficient,order notional
          if e.code in over_flow and pos.q>0: pos.flag  = False
        else:
          log.exception('@open')

@keepAlive
def closing(): 
    while 1:
        n,pos = closes.get()
        try:  
          x = n.compute()
          bLog.info(x)
          transfer_to('SPOT',amt=.6*pos.profit) #babylonian
        except Exception as e:
          # bLog.exception("@close")
          if hasattr(e,'code'):
            bLog.error(f"@close {e.code} {e.message}")
            if e.code==-4045: cancel_order(pos.coin) #max stop Order  #-2021 would immediately trigger
          else:
            log.exception('@close')
        else:
          ic('Sell Successfull') 
          pos.flag = True 