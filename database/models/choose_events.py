from .events import Event
from .players import Player
from .types import *
from .enums import ChooseEventStatus


class ChooseEvent(Base):
    __tablename__ = 'choose_events'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    player_id: int = Column(BigInteger, ForeignKey("players.id"), index=True)
    event_id: int = Column(BigInteger, ForeignKey("events.id"), index=True)
    state: ChooseEventStatus = Column("state", Enum(ChooseEventStatus), default=ChooseEventStatus.ongoing)
    expired_at: datetime = Column(DateTime)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    players: Mapped[Player] = relationship(Player)
    events: Mapped[Event] = relationship(Event)
