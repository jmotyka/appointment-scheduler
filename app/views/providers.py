from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.providers import Provider
from app.controllers.providers import (
    get_or_create_provider
)
from app.schemas.providers import ProviderResponse

router = APIRouter()


@router.post("/providers", response_model=ProviderResponse)
def find_provider(first_name: str, last_name: str, db: Session = Depends(get_db)) -> Provider:
    return get_or_create_provider(db, first_name, last_name)