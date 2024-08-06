from qdrant_client_wrapper import QdrantClientWrapper
from vectorstore_retriever import VectorStoreRetriever
from rag.rag import run_rag

# Qdrant
qdrant_host = "http://3.38.106.92:6333/"
collection_name = "company_info"

# Qdrant 클라이언트 초기화
qdrant_client_wrapper = QdrantClientWrapper(qdrant_host, collection_name)

def run_llm(question: str):
    vector_store = qdrant_client_wrapper.get_client()
    retriever_instance = VectorStoreRetriever(vector_store)
    result = run_rag(retriever_instance.get_retriever(), question)
    print(result)

if __name__ == "__main__":
    run_llm("백엔드 개발자 5년차")
