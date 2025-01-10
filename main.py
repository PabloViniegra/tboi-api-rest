from fastapi import FastAPI, Depends
from src.database.db import Base, engine
from src.routers import item
from src.routers import chatbot
from src.routers import monster
import src.database.models
from fastapi.middleware.cors import CORSMiddleware
from auth import get_user

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item.router, dependencies=[Depends(get_user)])
app.include_router(chatbot.router, dependencies=[Depends(get_user)])
app.include_router(monster.router, dependencies=[Depends(get_user)])
