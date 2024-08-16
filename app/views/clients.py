from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.clients import Client
from app.controllers.clients import (
    get_or_create_client
)
from app.schemas.clients import ClientResponse

router = APIRouter()


@router.post("/clients", response_model=ClientResponse)
def find_client(first_name: str, last_name: str, db: Session = Depends(get_db)) -> Client:
    return get_or_create_client(db, first_name, last_name)
