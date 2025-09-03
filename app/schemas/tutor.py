from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID

class TutorBase(BaseModel):
    name: str
    cpf: constr(min_length=11, max_length=11) # Garante que o CPF tenha 11 dígitos
    phone: str
    pet_id: Optional[UUID] = None # O pet_id é opcional!

class TutorCreate(TutorBase):
    pass

class TutorUpdate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[constr(min_length=11, max_length=11)] = None
    phone: Optional[str] = None
    pet_id: Optional[UUID] = None

class TutorOut(TutorBase):
    id: UUID

    class Config:
        from_attributes = True