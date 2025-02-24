from .types import *
from .users import User


class Notification(Base):
    __tablename__ = "notifications"

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    message: str = Column(String, nullable=False)
    user_id: int = Column(BigInteger, ForeignKey("users.id"), index=True)
    is_checked: bool = Column(Boolean, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user: Mapped[User] = relationship(User)
