from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.providers import ProviderResponse
from app.schemas.clients import ClientResponse


class AppointmentResponse(BaseModel):
    id: int
    appointment_time: datetime
    created_time: datetime
    booked_time: Optional[datetime] = None
    reservation_confirmed: bool
    client: Optional[ClientResponse]
    provider: ProviderResponse

    class Config:
        orm_mode = True