from .types import *


class Partner(Base):
    __tablename__ = 'partners'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    info: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
