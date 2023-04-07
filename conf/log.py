"""
Logging Config

# https://docs.python.org/3/library/logging.config.html

"""
import logging

from icecream import ic, install
import logging as log
import logging.config as log_config

import time


def _prefix_time():
    return f"{time.strftime('%X')}"


def setup_log() -> [logging.Logger]:
    def _info(s):
        print(s)
        # alog.info(f'{s}')

    ic.configureOutput(prefix=_prefix_time, outputFunction=_info, includeContext=False)
    # install()

    # log.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(process)d %(name)s - %(levelname)s - %(
    # message)s ', datefmt='%d-%b-%y %H:%M:%S',level=log.INFO) log.basicConfig(level=log.INFO)

    # ic.configureOutput(outputFunction=info)
    log_config.fileConfig(fname='conf/log.conf', disable_existing_loggers=False)  # Auto calls basicConfig and mods
    alog = log.getLogger('app')
    return alog
