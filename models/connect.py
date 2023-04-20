import logging
import sys
from typing import Optional

import sqlalchemy.engine


def create_engine(pool_size=10, max_overflow=20, echo=True, **kwargs) -> Optional[sqlalchemy.engine.Engine]:
    from sqlalchemy import create_engine
    from conf.db import DATABASE_URL
    try:
        _engine = create_engine(DATABASE_URL, pool_size=pool_size, max_overflow=max_overflow, echo=echo, **kwargs)
    except Exception as e:
        logging.critical("Failed to connect to database.")
        logging.critical(f"{e}")
        sys.exit(0)
    else:
        return _engine
