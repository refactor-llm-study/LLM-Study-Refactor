from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from app_config import Config

class QdrantClientWrapper:
    def __init__(self, host, collection_name):
        self.client = QdrantClient(host)
        self.collection_name = collection_name
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=Config.OPENAI_API_KEY)

    def create_collection(self):
        """컬렉션을 생성합니다."""
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            print(f"Collection {self.collection_name} created successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")

    def get_client(self):
        """Qdrant Client 객체를 반환합니다."""
        return self.client

    def ensure_collection_exists(self):
        """컬렉션이 존재하는지 확인하고, 없으면 생성합니다."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                print(f"Collection {self.collection_name} does not exist. Creating collection...")
                self.create_collection()
            else:
                print(f"Collection {self.collection_name} already exists.")
        except UnexpectedResponse as e:
            print(f"Unexpected error while checking or creating collection: {e}")
            raise

    def search_collection(self, query):
        """검색을 수행하기 전에 컬렉션이 존재하는지 확인합니다."""
        try:
            self.ensure_collection_exists()  # 컬렉션이 없으면 생성

            # 검색 실행
            search_result = self.client.search(
                collection_name=self.collection_name,
                query=query
            )
            return search_result

        except UnexpectedResponse as e:
            if e.status_code == 404:
                print(f"Collection {self.collection_name} not found during search. Creating collection...")
                self.create_collection()
                return self.client.search(
                    collection_name=self.collection_name,
                    query=query
                )
            else:
                print(f"Unexpected error during search: {e}")
                raise

    def get_vector_store(self, collection_name=None):
        if not collection_name:
            collection_name = self.collection_name
        
        self.ensure_collection_exists()

        try:
            return QdrantVectorStore(
                client=self.client,
                collection_name=collection_name,
                embedding=self.embedding_model
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
        vector_store.add_documents(documents=documents)
        print(f"Documents added successfully to collection {self.collection_name}.")
