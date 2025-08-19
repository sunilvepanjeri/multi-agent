# 🚀 Multi Tool Agent

A **FastAPI-based multi-tool agent system** that supports document ingestion, vector search, intelligent query handling, and retrieval evaluation using **OpenAI** and **ChromaDB**.  

This project demonstrates how to build a modular **agent architecture** with multiple embedding backends, tool definitions, and automated evaluation pipelines.

---

## 📂 Project Breakdown

### ⚙️ Settings Management
- Environment variables are managed using **pydantic-settings**.  
- Configure your OpenAI key, model names, and other values in the `.env` file.  
- Settings are automatically loaded at runtime.

---

### 📥 Ingestion Layer
Two ingestion APIs allow you to store documents in **ChromaDB** using different embedding strategies:

1. **Sentence Transformer Embeddings**  
   - Uses ChromaDB’s default sentence transformer for embeddings.  
   - Stores the embeddings in a persistent client on disk.  

2. **OpenAI Embeddings**  
   - Uses OpenAI’s embedding models for ingestion.  
   - Stored in a separate persistent client for comparison.  

**Ingestion Process:**
- **Document Loader**: Uses `pymupdf` for TXT/document parsing.  
- **Chunking Strategy**: Fixed size chunks of **200 tokens** with **50 token overlap**.  
- **VectorStore**: Persistent client ensures embeddings are saved locally.  

---

### 🤖 Message Agent Layer
- Provides an API to handle **user queries**.  
- Accepts structured input via a **Pydantic model**.  
- Loads `bot.json` containing:
  - System instructions / LLM prompt.  
  - Tool definitions.  

**Agent Workflow:**
1. Initializes the `agent` object using `Agent` class with the system prompt, tool definitions, and chat history.  
2. The `run()` method calls the **OpenAI responses API** with:
   - query
3. LLM decides which tool to invoke in run method.  
4. The selected tool is dynamically executed and returns results.  
5. The agent run method recursively re-runs with updated chat history until a final output is generated.  

---

### 📊 Evaluation Layer
- Provides an API to **evaluate retrieval quality** from both embedding approaches (Sentence Transformer vs OpenAI Embeddings).  
- Measures:
  - **Best Model** (via LLM-as-a-judge).  
  - **Latency** (time required to retrieve chunks).  
- LLM outputs which embedding method is more suitable.  

---

## 🛠️ Tech Stack
- **FastAPI** – Async Web framework  
- **ChromaDB** – Vector database  
- **OpenAI** – LLM & embeddings  
- **pydantic-settings** – Settings management  
- **pymupdf** – Document loading  
- **uv** – Dependency management  
- **Docker** – Containerization

---

## 📑 APIs Overview
After starting the server, visit **Swagger UI** (`http://0.0.0.0:8000/docs`) to explore the 4 APIs:

1. `POST rag/chroma/ingest` – Ingest the data with default sentence transformer.  
2. `POST rag/chroma/ingest/openai` – Ingest the data with OpenAI embeddings.  
3. `POST rag/message-agent` – Query via Message Agent.  
4. `POST rag/evaluate` – Outputs Best Model for retrieval and latency.  

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/sunilvepanjeri/multi-agent.git
