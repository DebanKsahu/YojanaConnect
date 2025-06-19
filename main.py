from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from Database.Engine import engine
from Dashboard.Profile.profile import profile_router
from Auth.auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(auth_router,tags=["Auth"])
app.include_router(profile_router,tags=["Dashboard"])


@app.get('/')
def demo():
    return {'message' : 'HELLO FROM YOJANA CONNECT'}