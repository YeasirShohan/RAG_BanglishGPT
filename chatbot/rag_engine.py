from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

def answer_query(question, collection_name):
    vectordb = Chroma(
        collection_name=collection_name,
        embedding_function=OllamaEmbeddings(model="LLaMA3"),
        persist_directory="vectorstore/chroma_db"
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = Ollama(model="LLaMA3", temperature=0.1)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain({"query": question})
    answer = result["result"]
    source_docs = result["source_documents"]
    return answer, source_docs

def stream_llm_response(prompt, context):
    import requests
    import json

    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "LLaMA3",   # Use LLaMA3 here as well
        "messages": [
            {"role": "system", "content": "Answer based only on the given context"},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
        ],
        "stream": True
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)
    for line in response.iter_lines():
        if line:
            try:
                json_data = json.loads(line.decode("utf-8").replace("data: ", ""))
                if "message" in json_data:
                    yield json_data["message"]["content"]
            except Exception:
                continue
