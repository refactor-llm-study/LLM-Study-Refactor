from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore  # QdrantVectorStore import
from langchain_openai import OpenAIEmbeddings  # OpenAIEmbeddings import
from app_config import Config

class QdrantClientWrapper:
    def __init__(self, host, collection_name):
        self.client = QdrantClient(host)
        self.collection_name = collection_name
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=Config.OPENAI_API_KEY)  # OpenAI Embeddings 초기화

    def create_collection(self):
        """컬렉션을 생성합니다."""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # OpenAI Embeddings의 벡터 크기
            )
            print(f"Collection {self.collection_name} created successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")

    def get_client(self):
        return self.client

    def ensure_collection_exists(self):
        """컬렉션이 존재하는지 확인하고, 없으면 생성합니다."""
        try:
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists.")
        except Exception:
            print(f"Collection {self.collection_name} does not exist. Creating collection...")
            self.create_collection()

    def get_vector_store(self, collection_name=None):
        if not collection_name:
            collection_name = self.collection_name
        
        # 컬렉션이 존재하는지 확인
        self.ensure_collection_exists()

        try:
            return QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embedding_model  # embedding 매개변수로 전달
            )
        except ValueError as e:
            print(f"Error initializing QdrantVectorStore: {e}")
            self.recreate_collection()
            return QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embedding_model
            )

    def recreate_collection(self):
        """기존 컬렉션을 삭제하고 새로 생성합니다."""
        try:
            print(f"Recreating collection {self.collection_name}...")
            self.client.delete_collection(self.collection_name)
            self.create_collection()
        except Exception as e:
            print(f"Error recreating collection: {e}")

    def add_documents(self, documents):
        vector_store = self.get_vector_store()
        vector_store.add_documents(documents=documents)  # 벡터와 함께 문서를 추가
        print(f"Documents added successfully to collection {self.collection_name}.")
