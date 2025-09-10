from fastapi import FastAPI
from app.controllers import (
    user_controller,
    auth_controller,
    tutor_controller,
    pet_controller,
)
from app.database import Base, engine
from app.database import engine, Base
from app.models.user import User
from app.models.tutor import Tutor
from app.models.pet import Pet
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Austay API",
    description="API para gestão de pets e tutores.",
    version="0.1.0",
)

# 2. Defina de quais origens você quer aceitar requisições
#    Neste caso, o seu frontend React
origins = [
    "http://localhost:5173",
    # Você pode adicionar outras URLs aqui, como a do seu site em produção
]

# 3. Adicione o middleware ao seu app FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite as origens definidas acima
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(tutor_controller.router)
app.include_router(pet_controller.router)
