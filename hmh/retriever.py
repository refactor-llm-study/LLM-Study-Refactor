class Retriever:
    def __init__(self, qdrant_client_wrapper):
        self.qdrant_client = qdrant_client_wrapper.get_client()

    def get_point_from_collection(self, collection_name: str, query_vector: list, limit: int = 5):
        search_result = self.qdrant_client.search(
            collection_name=collection_name, query_vector=query_vector, limit=limit
        )
        for result in search_result:
            print(f"ID: {result.id}, Score: {result.score}, Payload: {result.payload}")
        return search_result
