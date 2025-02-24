from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlockUserBase(BaseModel):
    info: str

class BlockUserCreate(BlockUserBase):
    user_id: int

class BlockUserUpdate(BaseModel):
    info: Optional[str] = None

class BlockUserInDB(BlockUserBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BlockUserOut(BlockUserInDB):
    pass
