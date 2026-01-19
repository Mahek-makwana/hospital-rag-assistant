import os
import sys
import shutil
from typing import List

# Core LangChain Imports
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class HospitalRAGAssistant:
    def __init__(self, model_name: str = "llama3.2", embedding_model: str = "nomic-embed-text"):
        self.model = ChatOllama(model=model_name, temperature=0)
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        # Optimized chunking for short directory listings and tables
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=50
        )
        self.persist_directory = "./chroma_db"

    def _cleanup_db(self):
        """Removes existing vector database to ensure fresh ingestion."""
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)

    def ingest_document(self, file_path: str):
        """Loads and indexes a PDF document into ChromaDB."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self._cleanup_db()
        
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        chunks = self.text_splitter.split_documents(docs)
        
        vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        # Increased k to 5 to capture more relevant context for short snippets
        return vectorstore.as_retriever(search_kwargs={"k": 5})

    def get_chain(self, retriever):
        """Builds the LCEL (LangChain Expression Language) RAG chain."""
        template = """
        You are a specialized hospital information assistant. 
        Use the following context to answer the question accurately.
        If the answer is not in the context, politely state that the information is not available.

        Context:
        {context}

        Question: 
        {question}

        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)

        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.model
            | StrOutputParser()
        )

def main():
    # Path configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "hospital_data.pdf")
    
    try:
        assistant = HospitalRAGAssistant()
        
        print(f"[*] Processing document: {DATA_PATH}...")
        retriever = assistant.ingest_document(DATA_PATH)
        
        chain = assistant.get_chain(retriever)
        
        print("[+] System Ready.")
        
        # Professional test queries
        queries = [
            "Where is the Cardiology department and who is the lead?",
            "What are the hospital visiting hours?",
            "How much does an MRI scan cost and is it covered by insurance?"
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            print("Assistant: ", end="", flush=True)
            for chunk in chain.stream(query):
                print(chunk, end="", flush=True)
            print("\n" + "-"*30)

    except Exception as e:
        print(f"\n[!] Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()