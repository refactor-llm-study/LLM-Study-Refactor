import os
from qdrant_client_wrapper import QdrantClientWrapper
from langchain_qdrant import QdrantVectorStore
from vectorstore_retriever import VectorStoreRetriever
from rag.rag import run_rag
from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Qdrant
qdrant_host = "http://3.38.106.92:6333/"
collection_name = "company_info"

# Qdrant 클라이언트 초기화
qdrant_client_wrapper = QdrantClientWrapper(qdrant_host, collection_name)

def run_llm(question: str):
    client = qdrant_client_wrapper.get_client()
    vector_store = QdrantVectorStore(client=client, collection_name="collection_0826", embedding=OpenAIEmbeddings(model="text-embedding-3-small"))
    retriever_instance = VectorStoreRetriever(vector_store)
    documents = retriever_instance.get_retriever(k=10).invoke(question)
    result = run_rag(documents, question)
    print(result)

if __name__ == "__main__":
    run_llm("백엔드 개발자 5년차, AWS 사용 가능한 회사 추천해주세요. 재택근무 가능하면 더 좋아요!")
