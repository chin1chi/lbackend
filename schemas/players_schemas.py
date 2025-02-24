from pydantic import BaseModel, condecimal
from datetime import datetime, date
from typing import Optional, List

class PlayerBase(BaseModel):
    full_name: str
    sex: bool
    date_birthday: date
    points_value: int
    experience_value: int
    currency_value: condecimal( decimal_places=2)

class PlayerCreate(PlayerBase):
    user_id: int
    entertainments_tags: int

class PlayerUpdate(PlayerBase):
    full_name: Optional[str] = None
    sex: Optional[bool] = None
    date_birthday: Optional[date] = None
    points_value: Optional[int] = None
    experience_value: Optional[int] = None
    currency_value: Optional[condecimal(decimal_places=2)] = None

class PlayerInDB(PlayerBase):
    id: int
    user_id: int
    entertainments_tags: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PlayerOut(PlayerInDB):
    # Можете добавить сюда связанные объекты, если нужно
    history_events: Optional[List[int]] = None
    choose_events: Optional[List[int]] = None
    feedback_events: Optional[List[int]] = None
    entertainments: Optional[List[int]] = None
