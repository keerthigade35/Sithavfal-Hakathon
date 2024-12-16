import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class PDFVectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(model_name)
        
        self.dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        
        self.chunks = []
    
    def add_documents(self, documents):
        embeddings = self.embedding_model.encode(documents)
        
        self.index.add(embeddings)
        self.chunks.extend(documents)
    
    def search(self, query, top_k=3):
        query_embedding = self.embedding_model.encode([query])
        
        distances, indices = self.index.search(query_embedding, top_k)
        
        return [self.chunks[idx] for idx in indices[0]]