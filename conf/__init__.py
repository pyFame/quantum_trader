# from log import ic, bLog, log
#
# from binance_client import client, async_client
# from .log import log, blog, apl, dog, alog

from .log import setup_log
from .binance_client import client, async_client, gen_client

alog = setup_log()
