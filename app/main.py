from fastapi import FastAPI
from app.controllers import (
    user_controller,
    auth_controller,
    tutor_controller,
    pet_controller,
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Austay API",
    description="API para gestão de pets e tutores.",
    version="0.1.0",
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(tutor_controller.router)
app.include_router(pet_controller.router)
