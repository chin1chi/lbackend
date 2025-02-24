from .history_events import HistoryEvent
from .players import Player
from .types import *


class FeedbackEvent(Base):
    __tablename__ = 'feedback_events'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    player_id: int = Column(BigInteger, ForeignKey("players.id"), index=True)
    history_event_id: int = Column(BigInteger, ForeignKey("history_events.id"), index=True)
    rating: int | None = Column(SmallInteger, nullable=True)
    is_liked: bool = Column(Boolean, nullable=False)
    comment: str | None = Column(String, nullable=True)
    photo: list[str] | None = Column(ARRAY(String), nullable=True, default=[])
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    players: Mapped[Player] = relationship(Player)
    history_event: Mapped[HistoryEvent] = relationship(HistoryEvent)
