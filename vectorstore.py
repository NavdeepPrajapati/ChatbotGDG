import faiss 
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)

    def add_embeddings(self, embeddings):
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query_embedding, k=5):
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return indices, distances

# Testing the vector store
if __name__ == "__main__":
    store = VectorStore(768)
    store.add_embeddings([[0.1] * 768])  # Dummy embedding
    print(store.search([0.1] * 768))
