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
    # Verifica se o tutor existe
    db_tutor = db.get(Tutor, pet.tutor_id)
    if not db_tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tutor não encontrado."
        )

    db_pet = Pet(**pet.model_dump())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet
