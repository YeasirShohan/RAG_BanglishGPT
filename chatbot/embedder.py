from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import fitz  # PyMuPDF

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

def embed_and_store(chunks, collection_name, persist_dir="vectorstore/chroma_db"):
    embedding = OllamaEmbeddings(model="LLaMA3")
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding,
        collection_name=collection_name,
        persist_directory=persist_dir
    )
    vectordb.persist()

def extract_text_from_pdf(file_path):
    """
    Extracts all text from the given PDF file using PyMuPDF.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text
