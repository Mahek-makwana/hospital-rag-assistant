# 🏥 Hospital RAG Assistant

A professional-grade **Retrieval-Augmented Generation (RAG)** system designed to query hospital documentation and administrative directories locally. This project leverages **LangChain (LCEL)**, **Ollama**, and **ChromaDB** to provide high-precision answers while ensuring 100% data privacy.

---

## 💎 Industry-Trending Skills Demonstrated
This project showcases mastery in the following high-demand areas for AI and Machine Learning roles in 2026:

* **Advanced RAG Architecture:** Specialized implementation of document chunking (500-token windows) and semantic search optimization ($k = 5$).
* **AI Sovereignty & Privacy:** Deploying **Llama 3.2** and **Nomic Embeddings** locally, a critical requirement for healthcare and financial sectors.
* **Modern LangChain Stack:** Expert use of **LangChain Expression Language (LCEL)** for building robust, modular, and readable AI pipelines.
* **Vector Database Engineering:** Efficient document indexing and persistence management using **ChromaDB**.

---

## 🚀 Key Features
- **Data Privacy:** No internet connection or API keys required; all data stays on your local machine.
- **Table Awareness:** Optimized to handle complex hospital service tables and directory listings.
- **Real-Time Streaming:** Features a professional token-streaming output for a responsive assistant experience.
- **Automatic DB Cleanup:** Includes a smart system to refresh the vector store when document parameters change.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.10** or higher
- **Ollama** (installed and running)


### 2. Clone the Repository
```bash
git clone [https://github.com/Mahek-makwana/hospital-rag-assistant.git](https://github.com/Mahek-makwana/hospital-rag-assistant.git)

---
3. Setup Virtual Environment
Bash

# Create the environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
4. Install Dependencies
Bash

pip install -r requirements.txt
5. Pull AI Models
Ensure Ollama is running in the background, then run:

Bash

ollama pull llama3.2
ollama pull nomic-embed-text
📂 Usage
Place your hospital directory PDF in the data/ folder.

Ensure the file is named hospital_data.pdf.

Run the assistant:

Bash

python src/main.py
🏗️ Project Structure
Plaintext

hospital-rag-assistant/
├── data/               # Source PDF documents
├── src/                # Python source code (main.py)
├── requirements.txt    # Project dependencies
├── .gitignore          # Files to exclude from Git
└── README.md           # Project documentation
