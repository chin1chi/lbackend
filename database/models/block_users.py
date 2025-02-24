from .types import *
from .users import User


class BlockUser(Base):
    __tablename__ = 'block_users'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(BigInteger, ForeignKey('users.id', ondelete="cascade", onupdate="cascade"), index=True)
    info: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user: Mapped[User] = relationship(User)
