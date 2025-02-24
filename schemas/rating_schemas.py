from typing import List
from pydantic import BaseModel


class PlayerRating(BaseModel):
    position: int
    username: str
    points_value: int


class RatingResponse(BaseModel):
    status: int = 200
    status_text: str = "OK"
    data: List[PlayerRating]
