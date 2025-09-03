from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.models.user import User
from app.database import get_db
from app.utils.security import hash_password
from app.utils.dependencies import get_current_user
from typing import List
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Usuário"])        

# Rota pública para criar usuário
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )
    
    db_user = User(name=user.name, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- ENDPOINTS PROTEGIDOS ---

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user

@router.get("/", response_model=List[UserOut])
def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) 
):
    """Lista todos os usuários. Requer autenticação."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) 
):
    """Busca um usuário pelo ID. Requer autenticação."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID, 
    user_in: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Adicione uma verificação para permitir que apenas o próprio usuário ou um admin edite
    if user.id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para editar este usuário")

    if user_in.name is not None:
        user.name = user_in.name
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.password is not None:
        user.password = hash_password(user_in.password)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado")
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if user.id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não tem permissão para excluir este usuário")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


