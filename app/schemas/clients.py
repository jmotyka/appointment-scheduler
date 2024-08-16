from pydantic import BaseModel


class ClientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True