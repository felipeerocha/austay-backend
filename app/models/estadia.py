import uuid
from sqlalchemy import Column, ForeignKey, String, Float, Boolean, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


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
    valor_total = Column(Float, nullable=True) # Valor total pode ser nulo inicialmente
    observacoes = Column(String, nullable=True)
    
    # O default=False garante que sempre seja falso na criação
    pago = Column(Boolean, default=False, nullable=False) 

    pet = relationship("Pet", back_populates="estadias")
    tutor = relationship("Tutor") # Assumindo que Tutor não tem back_populates="estadias"
    
    # Novo relacionamento um-para-um com Pagamento
    pagamento = relationship("Pagamento", back_populates="estadia", uselist=False, cascade="all, delete-orphan")