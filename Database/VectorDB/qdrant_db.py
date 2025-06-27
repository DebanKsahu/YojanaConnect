from qdrant_client import QdrantClient
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings
from dotenv import load_dotenv

load_dotenv()


qdrant_client = QdrantClient(
    url= settings.QDRANT_CLUSTER_URL,
    api_key=settings.QDRANT_API_KEY,
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