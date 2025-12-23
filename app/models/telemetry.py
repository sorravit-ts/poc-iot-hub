from pydantic import BaseModel


class Telemetry(BaseModel):
    temperature: float
    humidity: float
