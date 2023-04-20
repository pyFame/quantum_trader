from sqlalchemy import Column, String

from . import Base


class Symbol(Base):
    __tablename__ = 'symbols'
    name = Column(String(9), primary_key=True)
    base_asset = Column(String(5))
    quote_asset = Column(String(5))
