from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Union # <--- 1. IMPORTADO AQUI
from uuid import UUID
from datetime import date # Importar date

from app.database import get_db
from app.models.estadia import Estadia
from app.models.pet import Pet
from app.models.tutor import Tutor
from app.models.pagamento import Pagamento
from app.schemas.estadia import EstadiaCreate, EstadiaUpdate, EstadiaOut
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/estadias", tags=["Estadias"])


# --- NOVA FUNÇÃO HELPER ---
def calcular_valor_total(
    data_entrada: date, data_saida: date, valor_diaria: float
) -> Union[float, None]: # <--- 2. ALTERADO AQUI
    """Calcula o valor total da estadia se a data de saída estiver presente."""
    if not data_saida or not data_entrada:
        return None  # Ainda não é possível calcular

    dias = (data_saida - data_entrada).days
    if dias <= 0:
        dias = 1  # Cobrar pelo menos 1 diária

    return dias * valor_diaria


@router.post("/", response_model=EstadiaOut, status_code=status.HTTP_201_CREATED)
def create_estadia(
    estadia: EstadiaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        db_pet = db.get(Pet, estadia.pet_id)
        if not db_pet:
            raise HTTPException(status_code=404, detail=f"Pet com id {estadia.pet_id} não encontrado.")

        db_tutor = db.get(Tutor, estadia.tutor_id)
        if not db_tutor:
            raise HTTPException(status_code=404, detail=f"Tutor com id {estadia.tutor_id} não encontrado.")

        # 1. Criar a estadia
        db_estadia = Estadia(**estadia.model_dump())
        
        # 2. Calcular o valor total (se data_saida foi fornecida na criação)
        valor_total_calculado = calcular_valor_total(
            db_estadia.data_entrada, 
            db_estadia.data_saida, 
            db_estadia.valor_diaria
        )
        db_estadia.valor_total = valor_total_calculado
        
        db.add(db_estadia)
        db.flush()  # Obter o db_estadia.id

        # 3. Criar o pagamento com o valor já calculado
        db_pagamento = Pagamento(
            estadia_id=db_estadia.id,
            status=False,
            valor=valor_total_calculado  # Sincroniza o valor
        )
        db.add(db_pagamento)

        db.commit()

        # Recarregar com relacionamentos (como estava antes)
        db.refresh(db_estadia)
        db_estadia_com_relacionamentos = (
            db.query(Estadia)
            .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
            .filter(Estadia.id == db_estadia.id)
            .first()
        )
        
        return db_estadia_com_relacionamentos

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# list_estadias e get_estadia (sem mudanças)
@router.get("/", response_model=List[EstadiaOut])
def list_estadias(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    estadias = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return estadias

@router.get("/{estadia_id}", response_model=EstadiaOut)
def get_estadia(
    estadia_id: UUID, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_estadia = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .filter(Estadia.id == estadia_id)
        .first()
    )
    if not db_estadia:
        raise HTTPException(status_code=404, detail="Estadia não encontrada.")
    return db_estadia


@router.put("/{estadia_id}", response_model=EstadiaOut)
def update_estadia(
    estadia_id: UUID,
    estadia: EstadiaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_estadia = db.get(Estadia, estadia_id)
    if not db_estadia:
        raise HTTPException(status_code=404, detail="Estadia não encontrada.")

    update_data = estadia.model_dump(exclude_unset=True)

    # 1. Aplicar as atualizações na estadia
    for key, value in update_data.items():
        setattr(db_estadia, key, value)

    # 2. Recalcular o valor total
    valor_total_calculado = calcular_valor_total(
        db_estadia.data_entrada, 
        db_estadia.data_saida, 
        db_estadia.valor_diaria
    )
    db_estadia.valor_total = valor_total_calculado

    # 3. Sincronizar com o pagamento
    db_pagamento = db_estadia.pagamento  # Acessa via relationship
    if db_pagamento:
        db_pagamento.valor = valor_total_calculado

        # Sincronizar 'pago' (lógica que já tínhamos)
        if "pago" in update_data:
            novo_status = update_data["pago"]
            db_pagamento.status = novo_status
            
            # Se "despagou", limpar dados de pagamento
            if novo_status == False:
                db_pagamento.meio_pagamento = None
                db_pagamento.data_pagamento = None

    db.commit()
    
    # Recarregar com relacionamentos
    db.refresh(db_estadia)
    db_estadia_out = (
        db.query(Estadia)
        .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
        .filter(Estadia.id == db_estadia.id)
        .first()
    )
    return db_estadia_out


@router.delete("/{estadia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estadia(
    estadia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_estadia = db.get(Estadia, estadia_id)
    if not db_estadia:
        raise HTTPException(status_code=404, detail="Estadia não encontrada.")
    
    # Graças ao 'ondelete="CASCADE"' no modelo Pagamento,
    # o pagamento associado será deletado automaticamente.
    db.delete(db_estadia)
    db.commit()
    return None