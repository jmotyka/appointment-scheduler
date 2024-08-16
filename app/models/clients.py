from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)

    appointments = relationship("Appointment", back_populates="client")
