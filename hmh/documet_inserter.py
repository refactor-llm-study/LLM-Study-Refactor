import json  # json 모듈 임포트
from langchain_core.documents import Document

class DocumentInserter:
    def __init__(self, qdrant_client_wrapper, mysql_client, table_name):
        self.qdrant_client_wrapper = qdrant_client_wrapper
        self.mysql_client = mysql_client
        self.table_name = table_name

    def insert_documents(self, limit=100):
        # MySQL에서 데이터 가져오기
        data = self.mysql_client.fetch_data(self.table_name, limit=limit)

        documents = []
        for record in data:
            # json 문자열을 딕셔너리로 변환
            json_data = json.loads(record["json"])
            json_data["id"] = record["id"]  # id 추가
            
            detail = json_data["detail"]
            documents.append(Document(page_content=detail, metadata=json_data))
        
        # 벡터화하여 Qdrant에 삽입
        self.qdrant_client_wrapper.add_documents(documents)
        print(f"Inserted {len(documents)} documents to collection {self.table_name}")
