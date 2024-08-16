from sqlalchemy.orm import Session

from app.models.providers import Provider


def get_provider_by_id(db_session: Session, provider_id: int) -> Provider | None:
    return (
        db_session
        .query(Provider)
        .filter(Provider.id == provider_id)
        .first()
    )


def get_provider_by_name(db_session: Session, first_name: str, last_name: str) -> Provider | None:
    return (
        db_session
        .query(Provider)
        .filter(
            Provider.first_name == first_name,
            Provider.last_name == last_name
        )
        .first()
    )


def create_provider(db_session: Session, first_name: str, last_name: str) -> Provider:
    provider = Provider(first_name=first_name, last_name=last_name)
    db_session.add(provider)
    db_session.commit()
    db_session.refresh(provider)
    return provider


def get_or_create_provider(db_session: Session, first_name: str, last_name: str) -> Provider:
    provider = get_provider_by_name(db_session, first_name, last_name)
    if not provider:
        return create_provider(db_session, first_name, last_name)
    return provider
