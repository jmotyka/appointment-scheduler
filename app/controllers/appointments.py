import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.appointments import Appointment
from app.models.providers import Provider

from app.controllers.clients import get_client_by_name
from app.controllers.providers import get_provider_by_id
from app.controllers.utils import round_time


def get_appointment(db_session: Session, appointment_id: int) -> Appointment:
    return (
        db_session
        .query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )


def get_available_appointments(db_session: Session) -> list[Appointment]:
    """
    Return all appointments that fit the following constraints:
        1. Are 24 hours in advance
        2. Do not have a reservation
    """
    return (
        db_session
        .query(Appointment)
        .filter(
            Appointment.appointment_time > (
                datetime.datetime.now() + datetime.timedelta(days=1)
            ),
            Appointment.booked_time == None
        )
    )


def create_appointments(
    db_session: Session,
    provider_id: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime
) -> None:
    """
    In 15 minute increments, add Appointment records
    related to a given provider.
    """
    provider = get_provider_by_id(db_session, provider_id)
    def create_appointment(appointment_time: datetime.datetime) -> None:
        appointment = Appointment(
            appointment_time=appointment_time,
            provider_id=provider.id
        )
        db_session.add(appointment)

    start_time_rounded = round_time(start_time)
    end_time_rounded = round_time(end_time)
    current_time = start_time_rounded

    with db_session:
        while current_time < end_time_rounded:
            create_appointment(current_time)
            current_time += datetime.timedelta(minutes=15)
        db_session.commit()
        db_session.refresh(provider)

    return db_session.query(Appointment).filter(Appointment.provider_id == provider.id)


def reserve_appointment(
    db_session: Session,
    first_name: str,
    last_name: str,
    appointment_id: int
) -> Appointment:
    client = get_client_by_name(db_session, first_name, last_name)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")

    appointment = get_appointment(db_session, appointment_id)
    appointment.client_id = client.id
    appointment.booked_time = datetime.datetime.now()

    with db_session:
        db_session.add(appointment)
        db_session.commit()

    return db_session.query(Appointment).filter(Appointment.id == appointment_id).first()


def confirm_appointment(
    db_session: Session,
    appointment_id: int
) -> Appointment:
    appointment = get_appointment(db_session, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    elif appointment.booked_time is None:
        raise HTTPException(status_code=404, detail="Reservation expired.")

    with db_session:        
        appointment.reservation_confirmed = True
        db_session.add(appointment)
        db_session.commit()
    
    return db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
