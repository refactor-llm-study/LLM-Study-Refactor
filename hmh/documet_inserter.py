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
            json_data = record["json"]
            data_dict = json.loads(json_data)
            detail = data_dict["detail"]
            documents.append(Document(page_content=detail, metadata=data_dict))
        
        # 벡터화하여 Qdrant에 삽입
        self.qdrant_client_wrapper.add_documents(documents)
        print(f"Inserted {len(documents)} documents to collection {self.table_name}")
