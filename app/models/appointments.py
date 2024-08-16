from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.clients import Client
from app.models.providers import Provider


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_time = Column(DateTime)
    created_time = Column(DateTime, default=func.now())
    booked_time = Column(DateTime, default=None, nullable=True)
    reservation_confirmed = Column(Boolean, default=False)

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))

    client = relationship("Client", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
