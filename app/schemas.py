from pydantic import BaseModel


class ResponseModel(BaseModel):
    detail: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "detail": "Response message"
            }
        }
