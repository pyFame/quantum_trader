"""
Logging Config

# https://docs.python.org/3/library/logging.config.html

"""

from icecream import ic
import logging as log
import logging.config as log_config

import time


def info(s):
    log.info(f'{s}')


def prefix_time():
    return f"{time.strftime('%X')}"


ic.configureOutput(prefix=prefix_time, outputFunction=info, includeContext=False)

# log.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(process)d %(name)s - %(levelname)s - %(
# message)s ', datefmt='%d-%b-%y %H:%M:%S',level=log.INFO) log.basicConfig(level=log.INFO)


ic.configureOutput(prefix=prefix_time, outputFunction=info, includeContext=False)
# ic.configureOutput(outputFunction=info)
log_config.fileConfig(fname='conf/log.conf', disable_existing_loggers=False)  # Auto calles basicConfig and mods
bLog = log.getLogger('binanceLogger')
