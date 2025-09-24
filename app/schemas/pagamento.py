from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class PagamentoBase(BaseModel):
    meio_pagamento: str
    data_pagamento: str


class PagamentoCreate(PagamentoBase):
    estadia_id: UUID


class PagamentoUpdate(BaseModel):
    status: Optional[str] = None
    meio_pagamento: Optional[str] = None
    data_pagamento: Optional[str] = None


class PagamentoOut(PagamentoBase):
    id: UUID
    estadia_id: UUID
    valor: float
    status: str

    class Config:
        from_attributes = True
