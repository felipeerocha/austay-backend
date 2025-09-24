import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Pagamento(Base):
    __tablename__ = "pagamento"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estadia_id = Column(UUID(as_uuid=True), ForeignKey("estadia.id"), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    meio_pagamento = Column(String, nullable=False)
    data_pagamento = Column(String, nullable=False)
