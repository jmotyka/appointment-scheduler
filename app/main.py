import logging

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends

from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

from app.background import remove_expired_appointments
from app.database import init_db, get_db, SQLALCHEMY_DATABASE_URL, SessionLocal
from app.models.appointments import Appointment
from app.views.appointments import router as appointment_router
from app.views.clients import router as client_router
from app.views.providers import router as provider_router

app = FastAPI()
logger = logging.getLogger(__name__)
sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

# Include the provider router
app.include_router(client_router, prefix="/api")
app.include_router(provider_router, prefix="/api")
app.include_router(appointment_router, prefix="/api")


# runner = BackgroundRunner(lookback=30, sleep_time=1)

@app.on_event("startup")
def startup_event():
    init_db()
    logging.info("Database initialized successfully")


@app.on_event("startup")
@repeat_every(seconds=5, logger=logger)
def remove_expired_tokens_task() -> None:
    with SessionLocal() as db:
        remove_expired_appointments(db, 0.1)


@app.get("/ping/")
def ping():
    return {"message": "Ping successful"}