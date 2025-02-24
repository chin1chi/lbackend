from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional, List


class EventBase(BaseModel):
    event_id: str
    partner_id: int
    name: str
    description: str
    entertainments_tag: Optional[int] = None
    media: Optional[str] = None
    inst: Optional[str] = None
    location: Optional[str] = None
    price: condecimal(decimal_places=2) = 0
    for_adults: bool
    schedule: Optional[str] = None
    accrued_points: int
    level_difficulty: int
    started_at: datetime
    expired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EventUpdate(BaseModel):
    partner_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    entertainments_tag: Optional[int] = None
    media: Optional[str] = None
    inst: Optional[str] = None
    location: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    for_adults: Optional[bool] = None
    schedule: Optional[str] = None
    accrued_points: Optional[int] = None
    level_difficulty: Optional[int] = None
    started_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class EventShortInfo(BaseModel):
    name: str
    description: str
    location: str


class PlayerRequest(BaseModel):
    player_id: int


class EventRequest(BaseModel):
    event_id: int


class CountEventsRequest(BaseModel):
    count_events: int


class EventInfo(BaseModel):
    id: int
    name: str
    description: str
    media: Optional[str] = None


class EventIdRequest(BaseModel):
    event_id: int


class EventResponse(BaseModel):
    status: int = 200
    status_text: str = "OK"
    data: List[EventInfo]


class EventDetailsResponce(BaseModel):
    name: str
    description: str
    location: str
    started_at: datetime
    expired_at: Optional[datetime] = None
    price: condecimal(decimal_places=2) = 0
    media: Optional[str] = None
    inst: Optional[str] = None
