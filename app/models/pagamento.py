import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Pagamento(Base):
    __tablename__ = "pagamento"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    estadia_id = Column(UUID(as_uuid=True), ForeignKey("estadia.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    valor = Column(Float, nullable=True) 
    
    # Alterado para Boolean e com default=False
    status = Column(Boolean, nullable=False, default=False) 
    
    # Campos preenchidos somente quando o status vira True
    meio_pagamento = Column(String, nullable=True)
    data_pagamento = Column(String, nullable=True)

    estadia = relationship("Estadia", back_populates="pagamento")