from fastapi import FastAPI
from app.controllers import user_controller, auth_controller, tutor_controller
from app.database import Base, engine
from app.database import engine, Base
from app.models.user import User
from app.models.tutor import Tutor
from app.models.pet import Pet

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Austay API",
    description="API para gestão de pets e tutores.",
    version="0.1.0"
)

app.include_router(user_controller.router)
app.include_router(auth_controller.router)
app.include_router(tutor_controller.router)
