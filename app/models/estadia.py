import uuid
from sqlalchemy import Column, ForeignKey, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Estadia(Base):
    __tablename__ = "estadia"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    data_entrada = Column(String, nullable=False)
    data_saida = Column(String, nullable=True)
    valor_diaria = Column(Float, nullable=False)
    observacoes = Column(String, nullable=True)
    pago = Column(Boolean, default=False)
