from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from datetime import date, timedelta
from typing import List

from app.database import get_db
from app.models.estadia import Estadia
from app.schemas.dashboard import (
    DashboardOut, CheckInOutSummary, PetHospedadoOut, MoreDaysOut,
    MovimentacoesPorDataOut, MovimentacaoDetalhe
)
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

CAPACIDADE_MAXIMA = 50

def get_checkins_checkouts_for_days(db: Session, hoje: date, start_day: int, num_days: int) -> List[CheckInOutSummary]:
    result = []
    for i in range(start_day, start_day + num_days):
        data_futura = hoje + timedelta(days=i)
        
        checkins = (
            db.query(Estadia)
            .filter(Estadia.data_entrada == data_futura)
            .count()
        )
        
        checkouts = (
            db.query(Estadia)
            .filter(
                and_(
                    Estadia.data_saida.isnot(None),
                    Estadia.data_saida == data_futura
                )
            )
            .count()
        )
        
        result.append(
            CheckInOutSummary(
                date=data_futura,
                check_ins=checkins,
                check_outs=checkouts
            )
        )
    return result

@router.get("/", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hoje = date.today()
    proximos_dias = 7
    
    total_pets_hospedados = (
        db.query(Estadia)
        .filter(
            and_(
                Estadia.data_entrada <= hoje,
                or_(
                    Estadia.data_saida.is_(None),
                    Estadia.data_saida >= hoje
                )
            )
        )
        .count()
    )
    
    taxa_ocupacao = (total_pets_hospedados / CAPACIDADE_MAXIMA) * 100 if CAPACIDADE_MAXIMA > 0 else 0
    
    checkins_hoje = (
        db.query(Estadia)
        .filter(Estadia.data_entrada == hoje)
        .count()
    )
    
    checkouts_hoje = (
        db.query(Estadia)
        .filter(
            and_(
                Estadia.data_saida.isnot(None),
                Estadia.data_saida == hoje
            )
        )
        .count()
    )
    
    checkins_checkouts_hoje = CheckInOutSummary(
        date=hoje,
        check_ins=checkins_hoje,
        check_outs=checkouts_hoje
    )
    
    checkins_checkouts_proximos_dias = get_checkins_checkouts_for_days(db, hoje, 1, proximos_dias)
    
    return DashboardOut(
        total_pets_hospedados=total_pets_hospedados,
        taxa_ocupacao=round(taxa_ocupacao, 2),
        checkins_checkouts_hoje=checkins_checkouts_hoje,
        checkins_checkouts_proximos_dias=checkins_checkouts_proximos_dias,
        capacidade_maxima=CAPACIDADE_MAXIMA
    )

@router.get("/pets-hospedados", response_model=List[PetHospedadoOut])
def get_pets_hospedados(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hoje = date.today()
    
    estadias = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .filter(
            and_(
                Estadia.data_entrada <= hoje,
                or_(
                    Estadia.data_saida.is_(None),
                    Estadia.data_saida >= hoje
                )
            )
        )
        .order_by(Estadia.data_entrada.desc())
        .all()
    )
    
    pets_hospedados = []
    for estadia in estadias:
        pets_hospedados.append(
            PetHospedadoOut(
                estadia_id=estadia.id,
                pet_id=estadia.pet.id,
                pet_nome=estadia.pet.nome,
                tutor_nome=estadia.tutor.name,
                data_entrada=estadia.data_entrada,
                data_saida=estadia.data_saida,
                valor_diaria=estadia.valor_diaria,
                pago=estadia.pago
            )
        )
    
    return pets_hospedados

@router.get("/more-days", response_model=MoreDaysOut)
def get_more_days(
    start_day: int = Query(..., ge=1, description="Dia inicial (1 = amanhã)"),
    num_days: int = Query(..., ge=1, le=30, description="Número de dias a buscar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hoje = date.today()
    checkins_checkouts = get_checkins_checkouts_for_days(db, hoje, start_day, num_days)
    return MoreDaysOut(checkins_checkouts=checkins_checkouts)

@router.get("/movimentacoes/{data}", response_model=MovimentacoesPorDataOut)
def get_movimentacoes_por_data(
    data: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    checkins_estadias = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .filter(Estadia.data_entrada == data)
        .all()
    )
    
    checkouts_estadias = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .filter(
            and_(
                Estadia.data_saida.isnot(None),
                Estadia.data_saida == data
            )
        )
        .all()
    )
    
    checkins = []
    for estadia in checkins_estadias:
        hora_str = estadia.hora_inicio.strftime("%H:%M") if estadia.hora_inicio else None
        checkins.append(
            MovimentacaoDetalhe(
                estadia_id=estadia.id,
                pet_nome=estadia.pet.nome,
                tutor_nome=estadia.tutor.name,
                hora=hora_str,
                valor_diaria=estadia.valor_diaria,
                pago=estadia.pago
            )
        )
    
    checkouts = []
    for estadia in checkouts_estadias:
        hora_str = estadia.hora_final.strftime("%H:%M") if estadia.hora_final else None
        checkouts.append(
            MovimentacaoDetalhe(
                estadia_id=estadia.id,
                pet_nome=estadia.pet.nome,
                tutor_nome=estadia.tutor.name,
                hora=hora_str,
                valor_diaria=estadia.valor_diaria,
                pago=estadia.pago
            )
        )
    
    return MovimentacoesPorDataOut(
        data=data,
        check_ins=checkins,
        check_outs=checkouts
    )

