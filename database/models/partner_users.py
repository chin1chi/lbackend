from .partners import Partner
from .types import *
from .users import User


class PartnerUser(Base):
    __tablename__ = 'partner_users'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    partner_id: int = Column(BigInteger, ForeignKey('partners.id'), index=True)
    user_id: int = Column(BigInteger, ForeignKey('users.id'), index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    user: Mapped[User] = relationship(User)
    partner: Mapped[Partner] = relationship(Partner)
