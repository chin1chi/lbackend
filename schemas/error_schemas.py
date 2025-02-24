from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: int
    status_text: str
    detail: str = None


class InternalServerErrorResponse(ErrorResponse):
    status: int = 500
    status_text: str = "Internal Server Error"


class NotFoundErrorResponse(ErrorResponse):
    status: int = 404
    status_text: str = "Not Found"


class BadRequestErrorResponse(ErrorResponse):
    status: int = 400
    status_text: str = "Bad Request"


class SuccessResponse(BaseModel):
    status: int = 200
    status_text: str = "OK"
