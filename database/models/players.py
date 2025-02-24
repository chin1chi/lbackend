from .entertainments import Entertainment
from .types import *
from .users import User


class Player(Base):
    __tablename__ = 'players'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    full_name: str = Column(String, nullable=False)
    sex: bool = Column(Boolean, nullable=False)
    date_birthday: datetime = Column(DateTime, nullable=False)
    entertainments_tags: list[int] = Column(ARRAY(BigInteger), nullable=False, default=[])
    points_value: int = Column(BigInteger, nullable=False)
    experience_value: int = Column(BigInteger, nullable=False)
    currency_value: Decimal = Column(DECIMAL, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user: Mapped[User] = relationship(User)
    # entertainment: Mapped[Entertainment] = relationship(Entertainment)
