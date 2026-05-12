from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(..., examples=["Incident not found"])
    status_code: int = Field(..., examples=[404])
    error: str = Field(..., examples=["HTTP_ERROR"])
