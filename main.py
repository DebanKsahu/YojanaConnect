from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from routes.ProfileRouter import router as UserRouter
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from Database.Engine import engine
from auth.auth import auth_router

@asynccontextmanager
async def onAppStartUp(app : FastAPI):
    print("FastAPI app is starting")
    ##db connection to be done here
    yield
    print("FastAPI is shutting down")

app = FastAPI(lifespan=onAppStartUp)



@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
app = FastAPI(lifespan=lifespan)




@app.get('/')
def demo():
    return {'message' : 'HELLO FROM YOJANA CONNECT'}

app.include_router(UserRouter , prefix='/user')
app.include_router(router=auth_router, tags=["Auth"])

