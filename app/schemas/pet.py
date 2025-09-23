from pydantic import BaseModel, constr
from typing import Optional, List
from uuid import UUID

class TutorPetOut(BaseModel):
    id: UUID
    name: str
    class Config:
        from_attributes = True

class PetBase(BaseModel):
    nome: str
    especie: str
    raca: str
    nascimento: Optional[str] = None
    sexo: str
    vermifugado: Optional[bool] = None
    vacinado: Optional[bool] = None

class PetCreate(PetBase):
    tutor_ids: List[UUID]

class PetUpdate(BaseModel):
    nome: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    nascimento: Optional[str] = None
    sexo: Optional[str] = None
    vermifugado: Optional[bool] = None
    vacinado: Optional[bool] = None
    tutor_ids: Optional[List[UUID]] = None

class PetOut(PetBase):
    id: UUID
    tutors: List[TutorPetOut] = []

    class Config:
        from_attributes = True
