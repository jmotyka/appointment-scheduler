import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointments import Appointment


def remove_expired_appointments(db_session: Session, lookback_minutes: int):
    with db_session:
        lookback = datetime.datetime.now() - datetime.timedelta(minutes=lookback_minutes)
        print(f"Looking up reservations that occurred before {lookback}")
        appointments = (
            db_session
            .query(Appointment)
            .filter(
                Appointment.reservation_confirmed == False,
                Appointment.booked_time is not None,
                Appointment.booked_time <= lookback
            )
            .all()
        )
        print(f"Removing {len(appointments)} reservations")
        for appointment in appointments:
            appointment.client_id = None
            appointment.booked_time = None
            db_session.add(appointment)
        
        db_session.commit()