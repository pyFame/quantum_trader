# from log import ic, alog, log
#
# from binance_client import client, async_client
# from .log import log, alog, apl, dog, alog

from .binance_client import client, async_client, gen_client
from .log import setup_log

alog = setup_log()

# import os
#
# os.system("mkdir -p $HOME/.postgresql")
# shutil.copyfile("conf/coachroach.crt", "$HOME/.postgresql", follow_symlinks=False)
# curl --create-dirs -o $HOME/.postgresql/root.crt 'https://cockroachlabs.cloud/clusters/d941e2cf-f8bf-4eb0-a015-f9cba09d25e5/cert'
# FIXME downlading is easier
