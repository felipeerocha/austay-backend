from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, time

# Schemas PetSimpleOut e TutorSimpleOut (sem mudanças)
class PetSimpleOut(BaseModel):
    id: UUID
    nome: str 
    class Config:
        from_attributes = True

class TutorSimpleOut(BaseModel):
    id: UUID
    name: str
    class Config:
        from_attributes = True

# --- Schemas Estadia ---

class EstadiaBase(BaseModel):
    data_entrada: date
    data_saida: Optional[date] = None
    hora_inicio: time
    hora_final: Optional[time] = None
    valor_diaria: float
    observacoes: Optional[str] = None


class EstadiaCreate(EstadiaBase):
    pet_id: UUID
    tutor_id: UUID


class EstadiaUpdate(BaseModel):
    data_saida: Optional[date] = None
    hora_final: Optional[time] = None
    observacoes: Optional[str] = None
    valor_diaria: Optional[float] = None
    pago: Optional[bool] = None


class EstadiaOut(EstadiaBase):
    id: UUID
    pago: bool
    valor_total: float
    pet: PetSimpleOut
    tutor: TutorSimpleOut

    class Config:
        from_attributes = True