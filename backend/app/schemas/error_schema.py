from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "detail": "Incident not found",
                    "status_code": 404,
                    "error": "HTTP_ERROR",
                }
            ]
        }
    )

    detail: str = Field(..., description="Human-readable error detail.", examples=["Incident not found"])
    status_code: int = Field(..., description="HTTP status code returned by the API.", examples=[404])
    error: str = Field(..., description="Internal error category.", examples=["HTTP_ERROR"])
