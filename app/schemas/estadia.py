from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class EstadiaBase(BaseModel):
    data_entrada: str
    data_saida: Optional[str] = None
    valor_diaria: float
    observacoes: Optional[str] = None


class EstadiaCreate(EstadiaBase):
    pet_id: UUID


class EstadiaUpdate(BaseModel):
    data_saida: Optional[str] = None
    observacoes: Optional[str] = None
    valor_diaria: Optional[float] = None


class EstadiaOut(EstadiaBase):
    id: UUID
    pet_id: UUID
    pago: bool

    class Config:
        from_attributes = True
