import datetime
import pytest

from app.database import SessionLocal, engine

from app.models.base import Base
from app.models.providers import Provider
from app.models.clients import Client
from app.models.appointments import Appointment


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield  # Run tests
    Base.metadata.drop_all(bind=engine)


def test_provider_model():
    with SessionLocal() as session:
        provider = Provider(first_name="Jared", last_name="Goff")
    
        session.add(provider)
        session.commit()
    
        assert provider.id == 1
        assert provider.first_name == "Jared"
        assert provider.last_name == "Goff"


def test_client_model():
    with SessionLocal() as session:
        client = Client(first_name="Jahmyr", last_name="Gibbs")

        session.add(client)
        session.commit()

        assert client.id == 1
        assert client.first_name == "Jahmyr"
        assert client.last_name == "Gibbs"


def test_appointment_model():
    with SessionLocal() as session:
        provider = Provider(first_name="Jared", last_name="Goff")
        client = Client(first_name="David", last_name="Montgomery")

        session.add(provider)
        session.add(client)
        session.commit()

        appointment_time = datetime.datetime(2024, 9, 8, 20, 20, 00)
        appointment = Appointment(
            appointment_time=appointment_time,
            client_id=client.id,
            provider_id=provider.id
        )

        session.add(appointment)
        session.commit()

        assert appointment.id == 1
        assert appointment.appointment_time == appointment_time
        assert appointment.booked_time == None

        assert appointment.provider.first_name == "Jared"
        assert appointment.provider.last_name == "Goff"

        assert appointment.client.first_name == "David"
        assert appointment.client.last_name == "Montgomery"
        
    