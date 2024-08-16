import datetime
import pytest

from app.database import SessionLocal, engine

from app.models.base import Base
from app.models.appointments import Appointment
from app.models.providers import Provider
from app.models.clients import Client

from app.background import remove_expired_appointments

from app.controllers.appointments import (
    get_appointment,
    get_available_appointments,
    create_appointments,
    reserve_appointment,
    confirm_appointment
)
from fastapi import HTTPException


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_appointment():
    with SessionLocal() as session:
        appointment = Appointment(appointment_time=datetime.datetime.now(), provider_id=1)
        session.add(appointment)
        session.commit()
        
        result = get_appointment(session, appointment.id)
        assert result == appointment


def test_get_available_appointments():
    with SessionLocal() as session:
        now = datetime.datetime.now()
        future_time = now + datetime.timedelta(days=2)
        past_time = now - datetime.timedelta(days=2)
        
        future_appointment = Appointment(appointment_time=future_time, booked_time=None)
        past_appointment = Appointment(appointment_time=past_time, booked_time=None)
        session.add_all([future_appointment, past_appointment])
        session.commit()
        
        result = get_available_appointments(session)
        assert future_appointment in result
        assert past_appointment not in result


def test_create_appointments():
    with SessionLocal() as session:
        provider = Provider(first_name="John", last_name="Smith")
        session.add(provider)
        session.commit()

    with SessionLocal() as session:
        provider_id = 1
        start_time = datetime.datetime(2024, 8, 1, 10, 0)
        end_time = datetime.datetime(2024, 8, 1, 12, 0)
        appointments = create_appointments(session, provider_id, start_time, end_time)
        
        assert appointments.count() == 9

def test_reserve_appointment():
    with SessionLocal() as session:
        provider = Provider(first_name="John", last_name="Smith")
        client = Client(first_name="John", last_name="Doe")
        appointment = Appointment(provider_id=provider.id)
        session.add(provider)
        session.add(client)
        session.add(appointment)
        session.commit()

        reserved_appointment = reserve_appointment(session, "John", "Doe", appointment.id)
        
        assert reserved_appointment.client_id == 1
        assert reserved_appointment.booked_time is not None


def test_confirm_appointment():
    with SessionLocal() as session:
        provider = Provider(first_name="John", last_name="Smith")
        client = Client(first_name="John", last_name="Doe")
        appointment = Appointment(provider_id=provider.id)
        session.add(provider)
        session.add(client)
        session.add(appointment)
        session.commit()
        
        reserved_appointment = reserve_appointment(session, "John", "Doe", 1)
        confirmed_appointment = confirm_appointment(session, 1)
        
        assert confirmed_appointment.reservation_confirmed


def test_confirm_appointment_not_found():
    with SessionLocal() as session:
        provider = Provider(first_name="John", last_name="Smith")
        appointment = Appointment(provider_id=provider.id)
        session.add(provider)
        session.add(appointment)
        session.commit()

    with SessionLocal() as session:
        with pytest.raises(HTTPException) as excinfo: 
            confirm_appointment(session, 2)
        
        assert excinfo.value.status_code == 404
        assert "Reservation expired." == excinfo.value.detail


def test_remove_expired_reservations():
    with SessionLocal() as session:
        provider = Provider(first_name="John", last_name="Smith")
        appointment1 = Appointment(
            provider_id=provider.id,
            booked_time=datetime.datetime.now() - datetime.timedelta(minutes=60)
        )
        appointment2 = Appointment(
            provider_id=provider.id,
            booked_time=datetime.datetime.now() - datetime.timedelta(minutes=20)
        )
        session.add(provider)
        session.add(appointment1)
        session.add(appointment2)
        session.commit()

    remove_expired_appointments(SessionLocal(), lookback_minutes=30)

    with SessionLocal() as session:
        appointments = session.query(Appointment).all()

        assert appointments[0].booked_time is not None
        assert appointments[1].booked_time is None
