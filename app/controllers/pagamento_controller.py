from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.pagamento import Pagamento
from app.models.estadia import Estadia
from app.schemas.pagamento import PagamentoCreate, PagamentoUpdate, PagamentoOut
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("/", response_model=PagamentoOut, status_code=status.HTTP_201_CREATED)
def create_pagamento(
    pagamento: PagamentoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    estadia = db.get(Estadia, pagamento.estadia_id)
    if not estadia:
        raise HTTPException(status_code=404, detail="Estadia não encontrada.")

    existing_pagamento = (
        db.query(Pagamento).filter(Pagamento.estadia_id == pagamento.estadia_id).first()
    )
    if existing_pagamento:
        raise HTTPException(
            status_code=400, detail="Já existe um pagamento para esta estadia."
        )

    if estadia.pago:
        raise HTTPException(status_code=400, detail="Estadia já foi paga.")

    entrada = datetime.strptime(estadia.data_entrada, "%d/%m/%Y")
    saida = datetime.strptime(estadia.data_saida, "%d/%m/%Y")
    dias = (saida - entrada).days
    valor_total = dias * estadia.valor_diaria

    db_pagamento = Pagamento(
        estadia_id=pagamento.estadia_id,
        valor=valor_total,
        status="pago",
        meio_pagamento=pagamento.meio_pagamento,
        data_pagamento=pagamento.data_pagamento,
    )

    estadia.pago = True

    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.get("/", response_model=List[PagamentoOut])
def list_pagamentos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pagamentos = db.query(Pagamento).offset(skip).limit(limit).all()
    return pagamentos


@router.get("/{pagamento_id}", response_model=PagamentoOut)
def get_pagamento(
    pagamento_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_pagamento = db.get(Pagamento, pagamento_id)
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")
    return db_pagamento


@router.put("/{pagamento_id}", response_model=PagamentoOut)
def update_pagamento(
    pagamento_id: UUID,
    pagamento: PagamentoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_pagamento = db.get(Pagamento, pagamento_id)
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")

    update_data = pagamento.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_pagamento, key, value)

    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pagamento(
    pagamento_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_pagamento = db.get(Pagamento, pagamento_id)
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")

    estadia = db.get(Estadia, db_pagamento.estadia_id)
    if estadia:
        estadia.pago = False

    db.delete(db_pagamento)
    db.commit()
    return None
