# 🧠 BanglishGPT – Bangla-English PDF Chatbot using RAG + Django

BanglishGPT is a **Retrieval-Augmented Generation (RAG)** web application that allows users to upload Bangla or English PDFs and ask questions in natural language. The system answers contextually based on the uploaded documents using **local LLMs (like Mistral, LLaMA3, or Phi-3 via Ollama)** and **ChromaDB** as the vector store.

---

## Setup Guide

### 1. Clone the Repo
```bash
git clone https://github.com/yeasirshohan/banglishgpt.git
cd banglishgpt
```

### 2. Create Python Environment
```bash
python -m venv venv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Ollama & Pull a Model
```bash
ollama run llama3  
```

### 5. Run Django Server
```bash
python manage.py migrate
python manage.py runserver
```
### AND
'''
Click URL like http://127.0.0.1:8000/
'''
---

## 📦 Tools, Libraries, Packages

- **Django** – Web framework
- **Ollama** – Local LLM runner (LLaMA3)
- **ChromaDB** – Vector database
- **PyMuPDF** – PDF text extraction
- **LangChain** – RAG pipeline and embedding handling
- **HTML/CSS** – Chat UI
- **Postman / curl** – For API testing

---

## Sample Queries & Outputs

**PDF:** Bangla_HSC1st_paper.pdf 

**Query (Bangla):**  
`বাংলাদেশের স্বাধীনতা যুদ্ধ সম্পর্কে বলো।`  
**Output:**  
`১৯৭১ সালে বাংলাদেশের মুক্তিযুদ্ধ শুরু হয়...`

**Query (English):**  
`Tell me about the structure of the Bangladesh Constitution.`  
**Output:**  
`The Constitution of Bangladesh consists of...`

---

## API Documentation

**POST /api/upload/**  
- Upload a PDF file  
- Response: `collection_name`

**POST /api/ask/**  
- Payload: `{ "question": "...", "collection": "..." }`  
- Returns: `{ "answer": "..." }`  

---

## 📊 Evaluation Matrix (if implemented)
| Metric             | Result |
|--------------------|--------|
| Response Accuracy  | 85%    |
| Bangla Token Match | 90%    |
| Latency (Avg)      | 1.5s   |

---

## ❓Questions About the project

### 1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?

Used **PyMuPDF** (`fitz`) for efficient and reliable offline extraction. Some formatting issues (tables, columns) can occur in complex PDFs.

### 2. What chunking strategy did you choose? Why do you think it works well for semantic retrieval?

**Paragraph-based chunking** with newline separation. This preserves context better than sentence/character chunking for Bangla and English combined texts.

### 3. What embedding model did you use and why?

Used **Ollama's LLaMA3** via LangChain for embeddings. LLaMA3 performs well on multilingual text, is small, fast, and local.

### 4. How are you comparing the query with your stored chunks?

Using **cosine similarity** via **ChromaDB**. It’s fast and integrates easily with LangChain’s vector search tools.

### 5. How do you ensure meaningful comparison of question and chunks?

Text is pre-processed, chunked logically, embedded with semantic context, and retrieved using similarity metrics.  
If query is vague, the answer may be off-topic — prompt engineering or larger chunk overlap could help.

### 6. Do the results seem relevant?

Yes, for most cases. Relevance can improve with:
- More accurate chunking
- Larger document base
- Hybrid embedding (multilingual-specific models)

---