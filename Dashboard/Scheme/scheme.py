from fastapi import APIRouter,Depends,UploadFile,Form
from Auth.functions import oauth2_scheme, get_session, SECRET_KEY, ALGORITHM
from sqlmodel import Session, select, SQLModel
from Http_Exceptions.exceptions import user_not_found, wrong_authentication
from Database.VectorDB.qdrant_db import create_qdrant_vectorstore, embedding, sparse_embedding, qdrant_client
from Database.ORM_Models.scheme_models import SchemeInDB, SchemeExpose
from Database.ORM_Models.auth_models import UserInDB
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Dashboard.Scheme.functions import extract_text_from_pdf,input_formatter
from langchain_core.documents import Document
from dotenv import load_dotenv
from uuid import uuid4
from datetime import date
from Dashboard.Scheme.score_agent import agent_pipeline
from Dashboard.Scheme.qna_agent import agent_qna_pipeline
from qdrant_client.models import PointStruct
import jwt
import os

scheme_router = APIRouter()
load_dotenv()

class UserQuery(SQLModel):
    user_query: str

@scheme_router.post("/scheme/add_scheme")
async def add_scheme(file: UploadFile, scheme_name: str = Form(), sector: str = Form(), scheme_type: str = Form(), launch_date: date = Form(), website: str = Form(), session: Session = Depends(get_session)):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=250)
    temp_chunks = text_splitter.split_text(text=text)
    scheme_data = SchemeInDB(
            scheme_name=scheme_name,
            sector=sector,
            scheme_type=scheme_type,
            launch_date=launch_date,
            is_active=True,
            website=website
        )
    session.add(scheme_data)
    session.commit()
    session.refresh(scheme_data)
    documents = []
    uuids = []
    for index,chunk in enumerate(temp_chunks):
        document = Document(
            page_content=chunk,
            metadata = {
                "page_content": chunk,
                "file_name": str(file.filename),
                "text": str(chunk),  
                "scheme_name": str(scheme_name),
                "scheme_id": int(scheme_data.scheme_id)  
                }
            )
        documents.append(document)
        uuids.append(str(uuid4()))
    points = [
        PointStruct(
            id=uuids[i],
            vector={
                "dense": embedding.embed_query(documents[i].page_content,task_type="QUESTION_ANSWERING"),
                },
            payload=documents[i].metadata
        )
        for i in range(len(documents))
    ]

    qdrant_client.upsert(
        collection_name="test_pdfs_5",
        points=points
    )

    return {"message": "Scheme successfully added"}

@scheme_router.get("/scheme/show_all")
def show_all_scheme(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    qdrant = create_qdrant_vectorstore()
    all_scheme = session.exec(select(SchemeInDB)).all()
    all_user_criteria = user_detail.user_criteria
    user_input = input_formatter(all_user_criteria)
    result: list[SchemeExpose] = []
    for scheme in all_scheme:
        scheme_dict = scheme.model_dump()
        scheme_dict["match_score"] = agent_pipeline(scheme.scheme_id,qdrant,user_input)
        result.append(SchemeExpose(**scheme_dict))
    return result

@scheme_router.get("/scheme/{scheme_id}")
def scheme_qna_bot(scheme_id: int, user_query: UserQuery,  token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = jwt.decode(token,SECRET_KEY,[ALGORITHM])
    logged_user_name = payload.get("sub")
    logged_user_pk = payload.get("pk")
    user_detail = session.get(UserInDB,logged_user_pk)
    if not user_detail:
        raise user_not_found
    if user_detail.full_name!=logged_user_name:
        raise wrong_authentication
    qdrant = create_qdrant_vectorstore()
    all_user_criteria = user_detail.user_criteria
    formatted_user_data = input_formatter(all_user_criteria)
    result = agent_qna_pipeline(scheme_id,qdrant,user_query.user_query,formatted_user_data)
    return result.llm_response