from pydantic import BaseModel


class HealthCheckSchema(BaseModel):
    is_alive: bool = True
