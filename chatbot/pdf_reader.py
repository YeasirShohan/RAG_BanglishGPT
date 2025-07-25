import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Vectorstore persistent directory
VECTORSTORE_DIR = "vectorstore"

# Initialize embedding model and vectorstore
embedding_model = OllamaEmbeddings()
vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embedding_model)

def get_context_from_vectorstore(query, k=3):
    """
    Retrieves top-k relevant chunks from the vector store for the query.
    Returns the concatenated text context.
    """
    docs = vectorstore.similarity_search(query, k=k)
    context_texts = [doc.page_content for doc in docs]
    combined_context = "\n\n".join(context_texts)
    return combined_context
