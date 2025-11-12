from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.pagamento import Pagamento
from app.models.estadia import Estadia
# Schema PagamentoCreate agora só tem meio_pagamento e data_pagamento
from app.schemas.pagamento import PagamentoCreate, PagamentoUpdate, PagamentoOut
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/", response_model=PagamentoOut, status_code=status.HTTP_200_OK)
def create_pagamento(
    
    pagamento: PagamentoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Encontrar o pagamento (que já existe)
    db_pagamento = (
        db.query(Pagamento)
        .filter(Pagamento.estadia_id == pagamento.estadia_id)
        .first()
    )
    
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Registro de pagamento não encontrado.")

    if db_pagamento.status:
        raise HTTPException(status_code=400, detail="Pagamento já foi realizado.")

    # 2. Verificar se o valor a ser pago já foi calculado
    if db_pagamento.valor is None:
        raise HTTPException(
            status_code=400, 
            detail="Não é possível pagar. A estadia ainda não foi finalizada (sem data de saída)."
        )

    # 3. Efetuar o pagamento
    db_pagamento.status = True
    db_pagamento.meio_pagamento = pagamento.meio_pagamento
    db_pagamento.data_pagamento = pagamento.data_pagamento

    # 4. Sincronizar estadia
    db_pagamento.estadia.pago = True # Acessa via relationship

    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.get("/", response_model=List[PagamentoOut])
def list_pagamentos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pagamentos = db.query(Pagamento).offset(skip).limit(limit).all()
    return pagamentos


@router.get("/{pagamento_id}", response_model=PagamentoOut)
def get_pagamento(
    pagamento_id: UUID, db: Session = Depends(get_db),
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
    
    # *** LÓGICA DE SINCRONIZAÇÃO ***
    if "status" in update_data:
        novo_status = update_data["status"]
        
        # Carregar a estadia associada
        estadia = db_pagamento.estadia # Usando o relationship
        if estadia:
            estadia.pago = novo_status
            
        # Se estiver "despagando" (False), limpar os dados do pagamento
        if novo_status == False:
            db_pagamento.valor = None
            db_pagamento.valor_total = None
            db_pagamento.meio_pagamento = None
            db_pagamento.data_pagamento = None

    # Aplicar as atualizações no pagamento
    for key, value in update_data.items():
        setattr(db_pagamento, key, value)

    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


# Este endpoint agora "RESETA" o pagamento, em vez de deletar
@router.delete("/{pagamento_id}", response_model=PagamentoOut)
def delete_pagamento(
    pagamento_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_pagamento = db.get(Pagamento, pagamento_id)
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado.")

    # Sincronizar estadia
    estadia = db_pagamento.estadia
    if estadia:
        estadia.pago = False

    # Resetar o pagamento
    db_pagamento.status = False
    db_pagamento.valor = None
    db_pagamento.valor_total = None
    db_pagamento.meio_pagamento = None
    db_pagamento.data_pagamento = None

    db.commit()
    db.refresh(db_pagamento)
    
    # Retorna o pagamento resetado (em vez de 204 No Content)
    return db_pagamento