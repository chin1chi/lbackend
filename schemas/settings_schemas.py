from pydantic import BaseModel
from enum import Enum
from typing import Optional


class AppSettingTypeValue(str, Enum):
    status = "status"


class AppSettingBase(BaseModel):
    name: str
    value: str
    type_value: AppSettingTypeValue = AppSettingTypeValue.status  # По умолчанию 'status'


class AppSettingCreate(AppSettingBase):
    pass


class AppSettingUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    type_value: Optional[AppSettingTypeValue] = None


class AppSettingInDB(AppSettingBase):
    id: int
    class Config:
        orm_mode = True

# Схема для отображения настроек
class AppSettingOut(AppSettingInDB):
    pass
