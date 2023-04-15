from sqlalchemy import Boolean, Index
from sqlalchemy import Column, String

from models import Base


class Indicator(Base):
    __tablename__ = 'indicators'
    name = Column(String, nullable=False)
    active = Column(Boolean)

    # created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Indicator> {self.id} {self.name} {self.active}"

    __table_args__ = (
        Index('idx_indicator_name', name, unique=True),
        # Index('idx_name_email', name, email, unique=True),
    )
