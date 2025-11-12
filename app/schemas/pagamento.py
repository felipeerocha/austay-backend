from pydantic import BaseModel
from typing import Optional # Garanta que Optional está importado
from uuid import UUID

# Este schema é para a 'Realizar um Pagamento'
class PagamentoBase(BaseModel):
    meio_pagamento: str
    data_pagamento: str

class PagamentoCreate(PagamentoBase):
    estadia_id: UUID


class PagamentoUpdate(BaseModel):
    status: Optional[bool] = None
    meio_pagamento: Optional[str] = None
    data_pagamento: Optional[str] = None


# Este é o schema de OUTPUT (para GET)
class PagamentoOut(BaseModel):
    id: UUID
    estadia_id: UUID
    valor: Optional[float] = None
    status: bool

    # Campos que podem ser nulos no banco precisam ser Optional
    meio_pagamento: Optional[str] = None
    data_pagamento: Optional[str] = None

    class Config:
        from_attributes = True