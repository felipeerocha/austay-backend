from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.estadia import Estadia
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
    db_estadia = Estadia(**estadia.model_dump())
    db.add(db_estadia)
    db.commit()
    db.refresh(db_estadia)
    return db_estadia


@router.get("/", response_model=List[EstadiaOut])
def list_estadias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    estadias = db.query(Estadia).offset(skip).limit(limit).all()
    return estadias


@router.get("/{estadia_id}", response_model=EstadiaOut)
def get_estadia(
    estadia_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_estadia = db.get(Estadia, estadia_id)
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
    db.refresh(db_estadia)
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
