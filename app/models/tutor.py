import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Tutor(Base):
    __tablename__ = "tutors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

    # Relacionamento futuro com Pet (opcional por enquanto na lógica da API)
    # Usamos o tipo de dado UUID para a chave estrangeira.
    # O ForeignKey aponta para a coluna 'id' da futura tabela 'pets'.
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=True)