import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.models import pet_tutor_association

class Tutor(Base):
    __tablename__ = "tutors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

    pets = relationship(
        "Pet",
        secondary=pet_tutor_association,
        back_populates="tutors"
    )