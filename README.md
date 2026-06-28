# Secure RAG System with Guardrails & LLM-as-a-Judge

An enterprise-grade **Retrieval-Augmented Generation (RAG)** system built to demonstrate secure AI development. It implements **active guardrails** against malicious prompt injections, utilizes a protected **local vector database**, handles **LLM rate-limits/failures gracefully** with a custom fallback chain, and evaluates response quality using an automated **LLM-as-a-Judge testing suite**.

---

## 🛠️ Tech Stack & Pillars
*   **Web Framework:** FastAPI (Python 3.12+)
*   **Vector Database:** Qdrant (Persistent Local Storage)
*   **Embeddings & ML:** SentenceTransformers (`all-MiniLM-L6-v2`)
*   **Document Ingestion:** LangChain Text Splitters, PyPDF
*   **LLM API Engine:** OpenAI SDK with OpenRouter Fallbacks (GPT-OSS, Llama 3.3, Qwen, Nemotron)
*   **UI/UX Frontend:** HTML5, Modern Vanilla CSS (Sleek Dark Theme with live query trace logging)

---

## 🌟 Key Features
1.  🛡️ **Active Security Guardrails (`security.py`):** Real-time dual protection. Layer 1 detects prompt injections (e.g., *Ignore instructions*, *Reveal prompt*). Layer 2 blocks toxic keywords before executing DB database queries.
2.  💾 **Local Vector Storage (`02_embed_and_store.py`):** Encodes and stores PDF knowledge bases locally to protect data privacy using a persistent Qdrant instance.
3.  🔄 **Fault-Tolerance Fallbacks (`generate_module.py`):** Cascades systematically through backup LLMs sequentially when rate limits or API server overloads occur.
4.  📊 **LLM-as-a-Judge Quality Metrics (`06_evaluate.py`):** Automatically grades output alignment:
    *   **Faithfulness:** Verifies content only references retrieved source text (zeros hallucinations).
    *   **Relevancy:** Checks if answers directly solve the query.
5.  🎨 **Terminal Trace Frontend (`index.html`):** Beautiful dark-mode interface logging the RAG stages dynamically (**Security Check** $\rightarrow$ **Sources Retrieved** $\rightarrow$ **Grounded Generation**).

---

## 📂 Quick File Guide
*   `security.py`: Regex pattern guards and keyword blacklists.
*   `01_ingest.py`: PDF reader & chunk splitter logic.
*   `02_embed_and_store.py`: Generates vectors and sets up the database.
*   `03_retrieve.py`: Isolated retrieval logic querying Qdrant.
*   `generate_module.py`: The safe generation engine routing LLM selection.
*   `06_evaluate.py`: The automated test runner that scores responses.
*   `app.py`: FastAPI server routes of the REST API.

---

## ⚡ Quick Start

```bash
# 1. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add API Key inside a .env file
OPENROUTER_API_KEY=your_key_here

# 4. Ingest PDF & Build local Vector Database
python 02_embed_and_store.py

# 5. Start ASGI server
uvicorn app:app --reload
```
Navigate to `http://127.0.0.1:8000` inside your browser to interact with the interface!
