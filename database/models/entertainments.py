from .types import *


class Entertainment(Base):
    __tablename__ = 'entertainments'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    entertainment: str = Column(String, unique=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
