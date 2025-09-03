from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import verify_password, create_access_token
from app.schemas.token import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login. Recebe um JSON com email e senha.
    Retorna um token de acesso JWT.
    """
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    
    access_token_data = {"sub": user.email}
    access_token = create_access_token(data=access_token_data)

    return {"access_token": access_token, "token_type": "bearer"}