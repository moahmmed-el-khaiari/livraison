from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.db import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(String(36), primary_key=True, index=True)

    full_name = Column(String(120), nullable=False)
    phone = Column(String(30), nullable=False)

    street = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    zip = Column(String(20), nullable=True)
    country = Column(String(80), nullable=False)

    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
