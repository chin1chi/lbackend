from pydantic import BaseModel
from typing import Dict


class PlayerCategoriesResponse(BaseModel):
    data: Dict[str, bool]


class PlayerCategoryLikeResponse(BaseModel):
    data: Dict[str, bool]


class EntertainmentRequest(BaseModel):
    category_id: int


class LikeRequest(BaseModel):
    like: bool
