from pydantic import BaseModel, constr
from typing import Optional, List
from uuid import UUID

class PetTutorOut(BaseModel):
    id: UUID
    nome: str
    class Config:
        from_attributes = True

class TutorBase(BaseModel):
    name: str
    cpf: constr(min_length=11, max_length=11)
    phone: str

class TutorCreate(TutorBase):
    pass

class TutorUpdate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[constr(min_length=11, max_length=11)] = None
    phone: Optional[str] = None

class TutorOut(TutorBase):
    id: UUID
    pets: List[PetTutorOut] = []

    class Config:
        from_attributes = True