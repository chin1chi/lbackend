from .entertainments import Entertainment
from .partners import Partner
from .types import *


class Event(Base):
    __tablename__ = 'events'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    partner_id: int = Column(BigInteger, ForeignKey("partners.id"), index=True)
    name: str = Column(String, unique=True, nullable=False)
    description: str = Column(String, nullable=False)
    entertainments_tags: list[int] = Column(ARRAY(BigInteger),  nullable=False, default=[])
    media: str | None = Column(String, nullable=True)
    inst: str | None = Column(String, nullable=True)
    location: str | None = Column(String, nullable=True)
    price: Decimal | None = Column(DECIMAL, nullable=True)
    for_adults: bool = Column(Boolean, nullable=False)
    schedule: str | None = Column(String, nullable=True)
    accrued_points: int = Column(BigInteger, nullable=False)
    level_difficulty: int = Column(SmallInteger, nullable=False)
    started_at: datetime = Column(DateTime, default=datetime.utcnow)
    expired_at: datetime = Column(DateTime)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    partner: Mapped[Partner] = relationship(Partner)
    # entertainment: Mapped[Entertainment] = relationship(Entertainment)
