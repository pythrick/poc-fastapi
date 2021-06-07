from pydantic import BaseModel, Field


class ParamsSchema(BaseModel):
    limit: int = Field(ge=0, le=100, default=50)
    skip: int = Field(ge=0, default=0)
