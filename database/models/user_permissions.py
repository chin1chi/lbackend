from .types import *
from .users import User


class UserPermission(Base):
    __tablename__ = 'user_permissions'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(BigInteger, ForeignKey('users.id', ondelete="cascade", onupdate="cascade"), index=True)
    name_permission: str = Column(String, nullable=False)
    value: bool = Column(Boolean, default=False)
    expired_at: datetime = Column(DateTime)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user: Mapped[User] = relationship(User)
