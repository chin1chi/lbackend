from .types import *
from .enums import TypeValue


class AppSetting(Base):
    __tablename__ = 'app_settings'

    id: int = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False, index=True)
    value: str = Column(String, nullable=False)
    type_value: TypeValue = Column("type_value", Enum(TypeValue))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
