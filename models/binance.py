import logging as log
from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from models import Base

schema = "sqlite"

UUID_CLASS = UUID(as_uuid=True) if schema == "postgres" else String

log.warn(f"schema - {schema} uid {UUID_CLASS}")


class BinanceError(Base):
    __tablename__ = 'binance_errors'
    id = Column(String, primary_key=True, default=uuid4)
    binance_error_id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String)
