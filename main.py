from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from Database.Engine import engine
from Auth.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(router=auth_router, tags=["Auth"])
