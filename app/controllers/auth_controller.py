from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db
from app.models import user as models
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.schemas.token import LoginRequest, Token
from app.schemas import password_reset as schemas
from app.utils.security import (
    verify_password,
    create_access_token,
    generate_reset_token,
    hash_password,
)
from app.utils.email_sender import send_email

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    access_token_data = {"sub": user.email}
    access_token = create_access_token(data=access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        return {"msg": "Se um usuário com este e-mail existir, um código de verificação foi enviado."}

    token = generate_reset_token()
    reset = PasswordResetToken(user_id=user.id, token=token)
    db.add(reset)
    db.commit()
    db.refresh(reset)

    email_subject = "Recuperação de Senha - Suporte Austay"
    
    try:
        template_path = Path(__file__).parent.parent / "templates" / "password_reset.html"
        with open(template_path, "r", encoding="utf-8") as f:
            email_body = f.read()
        
        email_body = email_body.replace("{{ user_name }}", user.name or 'usuário')
        email_body = email_body.replace("{{ token }}", token)

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Template de e-mail não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar template de e-mail: {e}")
    
    send_email(to_email=user.email, subject=email_subject, body=email_body)
    
    return {"msg": "Código de verificação enviado para o e-mail"}

@router.post("/verify-token")
def verify_token(request: schemas.PasswordResetVerify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token_db = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.token == request.token,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not token_db:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    return {"msg": "Token válido"}

@router.post("/reset-password")
def reset_password(request: schemas.PasswordResetConfirm, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token_db = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.token == request.token,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not token_db:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado. Tente novamente.")

    user.password = hash_password(request.new_password)
    
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user.id).delete()
    
    db.commit()

    return {"msg": "Senha alterada com sucesso"}

