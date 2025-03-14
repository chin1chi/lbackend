from pydantic import BaseModel


class TokenRequest(BaseModel):
    token: str

class RefreshTokenRequest(BaseModel):
    access_token: str
