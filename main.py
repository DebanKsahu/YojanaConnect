from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from Database.Engine import engine
from Database.VectorDB.qdrant_db import qdrant_client
from qdrant_client import models
from qdrant_client.models import Distance, VectorParams
from Dashboard.Profile.profile import profile_router
from Dashboard.Scheme.scheme import scheme_router
from Auth.auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    existing_collections = qdrant_client.get_collections().collections
    collections_name = [col.name for col in existing_collections]
    if "test_pdfs_5" not in collections_name:
        qdrant_client.create_collection(
            collection_name="test_pdfs_5",
            vectors_config={"dense": VectorParams(size=768, distance=Distance.COSINE)},
            )
    schema = qdrant_client.get_collection("test_pdfs_5").payload_schema
    if "scheme_id" not in schema:
        qdrant_client.create_payload_index(
            collection_name="test_pdfs_5",
            field_name="scheme_id",
            field_schema=models.PayloadSchemaType.INTEGER
        )
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(auth_router,tags=["Auth"])
app.include_router(profile_router,tags=["Dashboard"])
app.include_router(scheme_router, tags=["Dashboard"])


@app.get('/')
def demo():
    return {'message' : 'HELLO FROM YOJANA CONNECT'}