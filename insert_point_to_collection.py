import os
import json
from dotenv import load_dotenv
from qdrant_client_wrapper import QdrantClientWrapper
from qdrant_client.http import models
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from openai import OpenAI
from uuid import uuid4
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# qdrant_client
qdrant_host = "http://3.38.106.92:6333/"
name = "company_info"

# Qdrant 클라이언트 초기화
qdrant_client_wrapper = QdrantClientWrapper(qdrant_host, "collection_0826")
qdrant_client = qdrant_client_wrapper.get_client()
qdrant_vector_store = QdrantVectorStore(client=qdrant_client, collection_name="collection_0826", embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

# def create_collection(collection_name: str):
#     qdrant_client.create_collection(
#         collection_name=collection_name,
#         vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
#     )
#     print(f"Created collection {collection_name}")


def insert_point_to_collection(collection_name: str):
    data_ids = sorted(os.listdir("wanted-crawling/data"))[:100]

    for id in data_ids:
        with open(f"wanted-crawling/data/{id}", "r") as f:
            data = f.read()
        id = int(id.split(".")[0])
        data = json.loads(data)
        detail = data["detail"]
        
        qdrant_vector_store.add_documents(documents=[Document(page_content=detail, metadata=data)])
        
        print(f"Inserted point {id} to collection {collection_name}")


def get_point_from_collection(collection_name: str, query_vector: list):
    search_result = qdrant_client.search(
        collection_name=collection_name, query_vector=query_vector, limit=5  # 가장 유사한 벡터 하나만 검색
    )

    # 검색 결과 출력
    for result in search_result:
        print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")
    return result.payload


if __name__ == "__main__":
    insert_point_to_collection("collection_0826")

    # query_sentence = """프론트엔드 개발자
    # 5년차 정도가 갈만한 회사 => JD 기준 경력은 3년 ~ 10년
    # 풀스택도 좋음
    # 대기업은 아니지만, 규모가 있는 스타트업에 가고 싶음
    # DAU나 MAU가 충분히 크다.
    # 프론트엔드 팀원이 10명 이상 또는 전체 팀 100명 이상
    # 도메인은 핀테크 등 금융에 대한 이해를 살릴 수 있는 도메인
    # """
    # query_vector = model.encode(query_sentence).tolist()
    # get_point_from_collection("whole_text", query_vector)