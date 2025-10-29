from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID

class CheckInOutSummary(BaseModel):
    date: date
    check_ins: int
    check_outs: int

class PetHospedadoOut(BaseModel):
    estadia_id: UUID
    pet_id: UUID
    pet_nome: str
    tutor_nome: str
    data_entrada: date
    data_saida: Optional[date]
    valor_diaria: float
    pago: bool
    
    class Config:
        from_attributes = True

class MovimentacaoDetalhe(BaseModel):
    estadia_id: UUID
    pet_nome: str
    tutor_nome: str
    hora: Optional[str]
    valor_diaria: float
    pago: bool
    
    class Config:
        from_attributes = True

class MovimentacoesPorDataOut(BaseModel):
    data: date
    check_ins: List[MovimentacaoDetalhe]
    check_outs: List[MovimentacaoDetalhe]
    
    class Config:
        from_attributes = True

class DashboardOut(BaseModel):
    total_pets_hospedados: int
    taxa_ocupacao: float
    checkins_checkouts_hoje: CheckInOutSummary
    checkins_checkouts_proximos_dias: List[CheckInOutSummary]
    capacidade_maxima: int
    
    class Config:
        from_attributes = True

class MoreDaysOut(BaseModel):
    checkins_checkouts: List[CheckInOutSummary]
    
    class Config:
        from_attributes = True

