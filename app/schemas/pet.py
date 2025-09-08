from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID


class PetBase(BaseModel):
    nome: str
    especie: str
    raca: str
    nascimento: Optional[str] = None
    sexo: str
    vermifugado: Optional[bool] = None
    vacinado: Optional[bool] = None
    tutor_id: UUID


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    nome: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    nascimento: Optional[str] = None
    sexo: Optional[str] = None
    vermifugado: Optional[bool] = None
    vacinado: Optional[bool] = None
    tutor_id: Optional[UUID] = None


class PetOut(PetBase):
    id: UUID

    class Config:
        from_attributes = True
