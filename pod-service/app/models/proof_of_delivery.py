from sqlalchemy import Column, String, DateTime, Text
from app.db import Base


class ProofOfDelivery(Base):
    __tablename__ = "proof_of_delivery"

    id = Column(String(36), primary_key=True)
    tracking_number = Column(String(64), unique=True, index=True, nullable=False)

    receiver_name = Column(String(120), nullable=False)
    receiver_id_number = Column(String(60), nullable=True)

    signature_base64 = Column(Text, nullable=True)     # simple (signature en base64)
    photo_url = Column(String(500), nullable=True)     # simple (un lien), optionnel

    note = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False)
