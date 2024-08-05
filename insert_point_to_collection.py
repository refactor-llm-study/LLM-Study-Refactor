import os
import json
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer


# qdrant_client
qdrant_host = "http://3.38.106.92:6333/"
name = "company_info"

# Qdrant 클라이언트 초기화
qdrant_client = QdrantClient(qdrant_host)
model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")


def create_collection(collection_name: str):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
    )


def insert_point_to_collection(collection_name: str):
    data_ids = os.listdir("company_info")

    for id in data_ids:
        try:
            with open(f"company_info/{id}", "r") as f:
                data = f.read()
            id = int(id.split(".")[0])
            data = json.loads(data)
            whole_text = "".join("".join(value) for value in data.values())
            vector = model.encode(whole_text).tolist()

            qdrant_client.upsert(
                collection_name=collection_name,
                points=[models.PointStruct(id=id, vector=vector, payload=data)],
            )
            print(f"Inserted point {id} to collection {collection_name}")
        except:
            print(f"Failed to insert point {id} to collection {collection_name}")


def get_point_from_collection(collection_name: str, query_vector: list):
    search_result = qdrant_client.search(
        collection_name=collection_name, query_vector=query_vector, limit=5  # 가장 유사한 벡터 하나만 검색
    )

    # 검색 결과 출력
    for result in search_result:
        print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")
    return result.payload

def get_query_vector(query_sentence: str):
    return model.encode(query_sentence).tolist()


if __name__ == "__main__":
    query_sentence = """프론트엔드 개발자
    5년차 정도가 갈만한 회사 => JD 기준 경력은 3년 ~ 10년
    풀스택도 좋음
    대기업은 아니지만, 규모가 있는 스타트업에 가고 싶음
    DAU나 MAU가 충분히 크다.
    프론트엔드 팀원이 10명 이상 또는 전체 팀 100명 이상
    도메인은 핀테크 등 금융에 대한 이해를 살릴 수 있는 도메인
    """
    query_vector = model.encode(query_sentence).tolist()
    get_point_from_collection("whole_text", query_vector)
