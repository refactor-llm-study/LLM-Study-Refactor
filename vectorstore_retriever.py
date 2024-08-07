class VectorStoreRetriever:
    def __init__(self, vector_store, **kwargs):
        self.vector_store = vector_store
        self.kwargs = kwargs

    def get_retriever(self):
        return self.vector_store.as_retriever(**self.kwargs)
