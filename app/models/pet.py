# app/models/pet.py
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Pet(Base):
    __tablename__ = "pets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)