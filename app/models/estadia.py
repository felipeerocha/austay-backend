import uuid
from sqlalchemy import Column, ForeignKey, String, Float, Boolean, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models.pet import Pet
from app.models.tutor import Tutor

class Estadia(Base):
    __tablename__ = "estadia"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    tutor_id = Column(UUID(as_uuid=True), ForeignKey("tutors.id"), nullable=False)

    data_entrada = Column(Date, nullable=False)
    data_saida = Column(Date, nullable=True)
    hora_inicio = Column(Time, nullable=False)
    hora_final = Column(Time, nullable=True)
    
    valor_diaria = Column(Float, nullable=False)
    observacoes = Column(String, nullable=True)
    pago = Column(Boolean, default=False)

    pet = relationship("Pet")
    tutor = relationship("Tutor")
    pet = relationship("Pet", back_populates="estadias") 
