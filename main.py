from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from routes.ProfileRouter import router as UserRouter

@asynccontextmanager
async def onAppStartUp(app : FastAPI):
    print("FastAPI app is starting")
    ##db connection to be done here
    yield
    print("FastAPI is shutting down")

app = FastAPI(lifespan=onAppStartUp)




@app.get('/')
def demo():
    return {'message' : 'HELLO FROM YOJANA CONNECT'}

app.include_router(UserRouter , prefix='/user')

