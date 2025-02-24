from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class NotificationBase(BaseModel):
    message: str
    is_checked: bool


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationUpdate(NotificationBase):
    message: Optional[str] = None
    is_checked: Optional[bool] = None


class NotificationInDB(NotificationBase):
    id: int
    message: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class IsCheckedNotificationRequest(BaseModel):
    is_checked: Optional[bool] = None


class NotificationRequest(BaseModel):
    notification_id: int


class NotificationInfo(BaseModel):
    id: int
    message: str


class NotificationResponse(BaseModel):
    status: int = 200
    status_text: str = "OK"
    data: List[NotificationInfo]
