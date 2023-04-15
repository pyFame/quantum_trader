import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy import Column, Integer, String

from models import Base


class Indicator(Base):
    __tablename__ = 'indicators'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Indicator> {self.id} {self.name} {self.active}"
