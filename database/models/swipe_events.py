from .events import Event
from .players import Player
from .types import *


class SwipeEvent(Base):
    __tablename__ = "swipe_events"

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    player_id: int = Column(BigInteger, ForeignKey("players.id"), index=True)
    event_id: int = Column(BigInteger, ForeignKey("events.id"), index=True)
    is_like: bool = Column(Boolean, nullable=False)

    # relationship
    player: Mapped[Player] = relationship(Player)
    event: Mapped[Event] = relationship(Event)
