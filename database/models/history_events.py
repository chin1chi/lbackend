from .events import Event
from .players import Player
from .types import *
from .enums import HistoryEventStatus


class HistoryEvent(Base):
    __tablename__ = 'history_events'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    player_id: int = Column(BigInteger, ForeignKey("players.id"), index=True)
    event_id: int = Column(BigInteger, ForeignKey("events.id"), index=True)
    state: HistoryEventStatus = Column("state", Enum(HistoryEventStatus), default=HistoryEventStatus.complete)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    player: Mapped[Player] = relationship(Player)
    event: Mapped[Event] = relationship(Event)
