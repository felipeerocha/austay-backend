from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    email: EmailStr
    token: str

class PasswordResetConfirm(BaseModel):
    email: EmailStr
    new_password: str
