from uuid import UUID, uuid4

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from . import Base


class Symbol(Base):
    __tablename__ = 'symbol'
    name = Column(String(9), primary_key=True)
    base_asset = Column(String(5))
    quote_asset = Column(String(5))


class FuturesSymbol(Base):
    __tablename__ = 'futures_symbols'
    futures_symbol_id = Column(Integer, primary_key=True)
    symbol_id = Column(String, ForeignKey('symbol.name'))
    isActive = Column(Boolean)
    hedge = Column(Boolean)
    symbol = relationship('Symbol', backref='futures_symbols')


class FuturesPosition(Base):
    __tablename__ = 'futures_positions'
    futures_position_id = Column(Integer, primary_key=True)
    futures_symbol_id = Column(Integer, ForeignKey('futures_symbols.futures_symbol_id'), nullable=False)
    mode = Column(String(4))
    disable_open = Column(Boolean)
    futures_symbol = relationship('FuturesSymbol', backref='futures_positions')


class FuturesAsset(Base):
    __tablename__ = 'futures_assets'
    futures_asset_id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)


class Indicator(Base):
    __tablename__ = 'indicators'
    indicator_id = Column(Integer, primary_key=True)
    name = Column(String)


class FuturesIndicator(Base):
    __tablename__ = 'futures_indicators'
    futures_indicator_id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey('indicators.indicator_id'), nullable=False)
    isActive = Column(Boolean)
    indicator = relationship('Indicator', backref='futures_indicators')

    def __repr__(self):
        return f"<Indicator> {self.id} {self.name} {self.isActive}"

    __table_args__ = (
        Index('idx_indicator_id', indicator_id, unique=True),
        Index('idx_indicator_active', indicator_id, isActive, unique=True),
    )


class BinanceError(Base):
    __tablename__ = 'binance_errors'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    binance_error_id = Column(Integer, primary_key=True)
    code = Column(Integer)
    description = Column(String)
