from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.estadia import Estadia
from app.models.pet import Pet
from app.models.tutor import Tutor
from app.schemas.estadia import EstadiaCreate, EstadiaUpdate, EstadiaOut
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/estadias", tags=["Estadias"])


@router.post("/", response_model=EstadiaOut, status_code=status.HTTP_201_CREATED)
def create_estadia(
    estadia: EstadiaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        # Verificar se pet existe
        db_pet = db.get(Pet, estadia.pet_id)
        if not db_pet:
            raise HTTPException(status_code=404, detail=f"Pet com id {estadia.pet_id} não encontrado.")

        # Verificar se tutor existe
        db_tutor = db.get(Tutor, estadia.tutor_id)
        if not db_tutor:
            raise HTTPException(status_code=404, detail=f"Tutor com id {estadia.tutor_id} não encontrado.")

        # Criar a estadia
        db_estadia = Estadia(**estadia.model_dump())
        
        db.add(db_estadia)
        db.commit()
        
        # Recarregar com relacionamentos
        db_estadia_com_relacionamentos = (
            db.query(Estadia)
            .options(joinedload(Estadia.pet), joinedload(Estadia.tutor))
            .filter(Estadia.id == db_estadia.id)
            .first()
        )
        
        if not db_estadia_com_relacionamentos:
            raise HTTPException(status_code=500, detail="Erro ao criar estadia")
        
        return db_estadia_com_relacionamentos
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# As outras rotas não precisam de mudança, pois a busca com joinedload já está correta
@router.get("/", response_model=List[EstadiaOut])
def list_estadias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
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
    estadia_id: UUID,
    db: Session = Depends(get_db),
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
    for key, value in update_data.items():
        setattr(db_estadia, key, value)

    db.commit()
    db.refresh(db_estadia) # Refresh aqui é seguro porque os relacionamentos não mudam
    
    return db_estadia


@router.delete("/{estadia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estadia(
    estadia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_estadia = db.get(Estadia, estadia_id)
    if not db_estadia:
        raise HTTPException(status_code=404, detail="Estadia não encontrada.")

    db.delete(db_estadia)
    db.commit()
    return None