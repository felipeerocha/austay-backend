import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID 
from app.database import Base
from app.models import pet_tutor_association

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
    
    tutors = relationship(
        "Tutor",
        secondary=pet_tutor_association,
        back_populates="pets"
    )
    
    estadias = relationship("Estadia", back_populates="pet")