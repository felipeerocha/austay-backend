import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    reset_tokens = relationship("PasswordResetToken", back_populates="user")

