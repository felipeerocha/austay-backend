from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate, TutorOut
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.schemas.pet import PetOut


router = APIRouter(prefix="/tutors", tags=["Tutores"])

@router.post("/", response_model=TutorOut, status_code=status.HTTP_201_CREATED)
def create_tutor(
    tutor: TutorCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_tutor_cpf = db.query(Tutor).filter(Tutor.cpf == tutor.cpf).first()
    if db_tutor_cpf:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    db_tutor = Tutor(**tutor.model_dump())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

@router.get("/", response_model=List[TutorOut])
def list_tutors(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tutors = db.query(Tutor).offset(skip).limit(limit).all()
    return tutors

@router.get("/{tutor_id}", response_model=TutorOut)
def get_tutor(
    tutor_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tutor = db.get(Tutor, tutor_id)
    if not db_tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")
    return db_tutor

@router.get("/{tutor_id}/pets", response_model=List[PetOut])
def get_tutor_pets(
    tutor_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_tutor = db.get(Tutor, tutor_id)
    if not db_tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tutor não encontrado."
        )
    return db_tutor.pets

@router.put("/{tutor_id}", response_model=TutorOut)
def update_tutor(
    tutor_id: UUID, 
    tutor: TutorUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tutor = db.get(Tutor, tutor_id)
    if not db_tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")

    update_data = tutor.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tutor, key, value)
    
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

@router.delete("/{tutor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tutor(
    tutor_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tutor = db.get(Tutor, tutor_id)
    if not db_tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")
    
    db.delete(db_tutor)
    db.commit()
    return None