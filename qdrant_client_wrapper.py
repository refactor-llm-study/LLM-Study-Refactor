from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

class QdrantClientWrapper:
    def __init__(self, host, collection_name):
        self.client = QdrantClient(host)
        self.collection_name = collection_name
        self.model = SentenceTransformer("distilbert-base-nli-stsb-mean-tokens")

    def create_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

    def get_client(self):
        return self.client
