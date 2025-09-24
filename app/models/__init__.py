from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

pet_tutor_association = Table(
    "pet_tutor_association",
    Base.metadata,
    Column("pet_id", UUID(as_uuid=True), ForeignKey("pets.id"), primary_key=True),
    Column("tutor_id", UUID(as_uuid=True), ForeignKey("tutors.id"), primary_key=True),
)

from .user import User
from .pet import Pet
from .tutor import Tutor
from .password_reset import PasswordResetToken
from .estadia import Estadia
from .pagamento import Pagamento