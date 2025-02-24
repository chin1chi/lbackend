from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserPermissionBase(BaseModel):
    name_permission: str
    value: bool = False

class UserPermissionCreate(UserPermissionBase):
    user_id: int

class UserPermissionUpdate(BaseModel):
    name_permission: Optional[str] = None
    value: Optional[bool] = None

class UserPermissionInDB(UserPermissionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    expired_at: datetime
    class Config:
        orm_mode = True

class UserPermissionOut(UserPermissionInDB):
    pass
