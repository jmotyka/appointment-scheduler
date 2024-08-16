import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.clients import Client
from app.models.providers import Provider
from app.models.appointments import Appointment

from app.controllers.clients import (
    get_or_create_client,
    get_client_by_name
)
from app.controllers.providers import (
    get_provider_by_name,
    get_or_create_provider
)
from app.controllers.appointments import (
    create_appointments,
    get_available_appointments,
    reserve_appointment,
    confirm_appointment
)
from app.schemas.appointments import AppointmentResponse
router = APIRouter()


@router.get("/appointments", response_model=list[AppointmentResponse])
def available_appointments(db: Session = Depends(get_db)):
    return get_available_appointments(db)


@router.post("/appointments/availability", response_model=list[AppointmentResponse])
def submit_provider_availability(
    first_name: str,
    last_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    db: Session = Depends(get_db)
) -> Appointment:
    provider = get_provider_by_name(db, first_name, last_name)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found.")

    return create_appointments(
        db,
        provider.id,
        start_time,
        end_time
    )

    
@router.post("/appointments/reserve", response_model=AppointmentResponse)
def reserve_appointment_for_client(
    first_name: str,
    last_name: str,
    appointment_id: int,
    db: Session = Depends(get_db)
):    
    return reserve_appointment(db, first_name, last_name, appointment_id)


@router.post("/appointments/confirm", response_model=AppointmentResponse)
def confirm_appointment_for_client(
    first_name: str,
    last_name: str,
    appointment_id: int,
    db: Session = Depends(get_db)
):
    client = get_client_by_name(db, first_name, last_name)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    
    return confirm_appointment(db, appointment_id, client.id)
