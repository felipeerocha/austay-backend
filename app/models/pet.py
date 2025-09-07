# app/models/pet.py
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Pet(Base):
    __tablename__ = "pets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False, index=True)
    especie = Column(String, nullable=False, index=True)
    raca = Column(String, nullable=False, index=True)
    nascimento = Column(String, nullable=True)
    sexo = Column(String, nullable=False, index=True)
    vermifugado = Column(Boolean, nullable=True)
    vacinado = Column(Boolean, nullable=True)
    tutor_id = Column(
        UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False, index=True
    )  # Relacionamento com Tutor
