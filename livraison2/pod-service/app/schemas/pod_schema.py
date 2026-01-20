from pydantic import BaseModel, Field
from typing import Optional


class CreatePodRequest(BaseModel):
    tracking_number: str = Field(min_length=3, max_length=64)
    receiver_name: str = Field(min_length=2, max_length=120)
    receiver_id_number: Optional[str] = Field(default=None, max_length=60)

    signature_base64: Optional[str] = None
    photo_url: Optional[str] = Field(default=None, max_length=500)

    note: Optional[str] = None


class PodOut(BaseModel):
    id: str
    tracking_number: str
    receiver_name: str
    receiver_id_number: Optional[str] = None

    signature_base64: Optional[str] = None
    photo_url: Optional[str] = None
    note: Optional[str] = None

    created_at: str
