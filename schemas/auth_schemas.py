from pydantic import BaseModel


class PhoneLoginRequest(BaseModel):
    phone: str

class CodeVerificationRequest(BaseModel):
    phone: str
    code: str

