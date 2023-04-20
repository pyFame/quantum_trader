from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship

from models import Base, Symbol


class FuturesSymbol(Base):
    __tablename__ = 'futures_symbols'
    futures_symbol_id = Column(Integer, primary_key=True)
    symbol_id = Column(String, ForeignKey('symbols.name'))
    isActive = Column(Boolean)
    hedge = Column(Boolean)
    symbol = relationship(Symbol, backref='futures_symbols')


class FuturesPosition(Base):
    __tablename__ = 'futures_positions'
    futures_symbol_id = Column(Integer, ForeignKey('futures_symbols.id'), nullable=False)
    mode = Column(String(4))
    disable_open = Column(Boolean)
    futures_symbol = relationship('FuturesSymbol', backref='futures_positions')


class FuturesAsset(Base):
    __tablename__ = 'futures_assets'
    name = Column(String)
    quantity = Column(Integer)


class FuturesIndicator(Base):
    __tablename__ = 'futures_indicators'
    indicator_id = Column(Integer, ForeignKey('indicators.id'), nullable=False)
    isActive = Column(Boolean)
    indicator = relationship('Indicator', backref='futures_indicators')

    def __repr__(self):
        return f"<Indicator> {self.id} {self.name} {self.isActive}"

    __table_args__ = (
        Index('idx_indicator_id', indicator_id, unique=True),
        Index('idx_indicator_active', indicator_id, isActive, unique=True),
    )
