from langchain_openai import OpenAIEmbeddings
from app_config import Config
from qdrant_client_wrapper import QdrantClientWrapper
from mysql_client import MySQLClient
from documet_inserter import DocumentInserter
from retriever import Retriever
from rag import run_rag

def main():
    # Qdrant 초기화
    qdrant_client_wrapper = QdrantClientWrapper(Config.QDRANT_HOST, Config.COLLECTION_NAME)
    
    # MySQL 클라이언트 초기화
    mysql_client = MySQLClient(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB
    )
    
    # 데이터 삽입 (최대 100개 레코드 가져오기)
    inserter = DocumentInserter(qdrant_client_wrapper, mysql_client, Config.TABLE_NAME)
    inserter.insert_documents(limit=100)
    
    # 데이터 검색 및 RAG 실행
    retriever = Retriever(qdrant_client_wrapper)
    
    # 쿼리 벡터 생성
    query = "백엔드 개발자 5년차, AWS 사용 가능한 회사 추천해주세요. 재택근무 가능하면 더 좋아요!"
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=Config.OPENAI_API_KEY)
    query_vector = embedding_model.embed_query(query)
    
    # 검색 수행
    results = retriever.get_point_from_collection(Config.COLLECTION_NAME, query_vector)
    documents = [result.payload for result in results]
    
    # RAG 실행
    result = run_rag(documents, query)
    print(result)

if __name__ == "__main__":
    main()

