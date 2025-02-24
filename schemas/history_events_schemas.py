from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class HistoryEventStatus(str, Enum):
    complete = "Завершено"
    cancel = "Отменено"

class HistoryDateFrom(BaseModel):
    dtfrom: datetime

class HistoryDateTo(BaseModel):
    dtto: datetime

class HistoryEventRequest(BaseModel):
    token: str
    dtfrom: datetime
    dtto: datetime


class HistoryEventInfo(BaseModel):
    name:str
    description:str
    created_at:datetime
    state: HistoryEventStatus

    class Config:
        from_attributes = True


class EventHistoryResponse(BaseModel):

    event_name: str
    description: str
    state: HistoryEventStatus
    class Config:
        from_attributes = True