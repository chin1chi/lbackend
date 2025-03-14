from pydantic import BaseModel


class PhoneLoginRequest(BaseModel):
    phone: str

class CodeVerificationRequest(BaseModel):
    phone: str
    code: str
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class CodeVerificationResponse(BaseModel):
    code: str

