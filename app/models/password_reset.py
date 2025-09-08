from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, default=lambda: datetime.datetime.utcnow() + datetime.timedelta(minutes=15))

    user = relationship("User", back_populates="reset_tokens")
