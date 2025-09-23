from pydantic import BaseModel, EmailStr
from uuid import UUID

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    user_id: UUID
    token: str

class PasswordResetConfirm(BaseModel):
    user_id: UUID
    token: str
    new_password: str
