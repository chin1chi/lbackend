from .types import *


class User(Base):
    __tablename__ = 'users'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username: str = Column(String, unique=True, nullable=False)
    phone_number: str = Column(String, unique=True, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
