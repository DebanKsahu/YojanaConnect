import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

qdrant_client = QdrantClient(
    url="https://9afad7e9-1087-4e91-ab4e-82aa44a699a0.us-west-2-0.aws.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.C7iVhsGpD3tsbRi3HWPPHaX5vV-9PHc-81mETxYUURI",
    timeout=30
)




embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
sparse_embedding = FastEmbedSparse(model_name="Qdrant/bm25")

def create_qdrant_vectorstore(qdrant_client: QdrantClient = qdrant_client, embedding: GoogleGenerativeAIEmbeddings = embedding, sparse_embedding: FastEmbedSparse = sparse_embedding):

    qdrant = QdrantVectorStore(
        client=qdrant_client,
        collection_name="test_pdfs_5",
        embedding=embedding,
        retrieval_mode=RetrievalMode.DENSE,
        vector_name="dense",
    )
    return qdrant