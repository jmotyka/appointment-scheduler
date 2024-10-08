from pydantic import BaseModel


class ProviderResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True