from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AddressCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=30)

    street: str = Field(min_length=2, max_length=200)
    city: str = Field(min_length=2, max_length=100)
    zip: Optional[str] = Field(default=None, max_length=20)
    country: str = Field(min_length=2, max_length=80)

    lat: Optional[float] = None
    lng: Optional[float] = None


class AddressOut(AddressCreate):
    id: str

    # Pydantic v2: permet de lire directement les attributs ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
