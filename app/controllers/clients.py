from sqlalchemy.orm import Session

from app.models.clients import Client


def get_client_by_id(db_session: Session, client_id: int) -> Client | None:
    return (
        db_session
        .query(Client)
        .filter(Client.id == client_id)
        .first()
    )


def get_client_by_name(db_session: Session, first_name: str, last_name: str) -> Client | None:
    return (
        db_session
        .query(Client)
        .filter(
            Client.first_name == first_name,
            Client.last_name == last_name
        )
        .first()
    )


def create_client(db_session: Session, first_name: str, last_name: str) -> Client:
    client = Client(first_name=first_name, last_name=last_name)
    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)
    return client


def get_or_create_client(db_session: Session, first_name: str, last_name: str) -> Client:
    client = get_client_by_name(db_session, first_name, last_name)
    if not client:
        return create_client(db_session, first_name, last_name)
    return client
