from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.pet import Pet
from app.models.tutor import Tutor
from app.schemas.pet import PetCreate, PetUpdate, PetOut
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/pets", tags=["Pets"])


@router.post("/", response_model=PetOut, status_code=status.HTTP_201_CREATED)
def create_pet(
    pet: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tutors_db = db.query(Tutor).filter(Tutor.id.in_(pet.tutor_ids)).all()

    if len(tutors_db) != len(pet.tutor_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Um ou mais tutores não foram encontrados.",
        )

    pet_data = pet.model_dump(exclude={"tutor_ids"})
    db_pet = Pet(**pet_data)

    db_pet.tutors.extend(tutors_db)

    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.get("/", response_model=List[PetOut])
def list_pets(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pets = db.query(Pet).offset(skip).limit(limit).all()
    return pets

@router.get("/{pet_id}", response_model=PetOut)
def get_pet(
    pet_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_pet = db.get(Pet, pet_id)
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")
    return db_pet
