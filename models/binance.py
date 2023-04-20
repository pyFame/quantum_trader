from uuid import UUID, uuid4

from sqlalchemy import Column, Integer, String

from models import Base


class BinanceError(Base):
    __tablename__ = 'binance_errors'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    binance_error_id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String)
