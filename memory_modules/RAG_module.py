from datetime import datetime
import os
import json
from dotenv import load_dotenv
import fitz
import time
from pathlib import Path
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from utils.prompts import RAG_prompts

#TODO: use openai from LLMCaller
load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vector_store = None

# Load OpenAI API key
def setup_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set in the .env file")
    os.environ["OPENAI_API_KEY"] = api_key

# Load and split documents from a URL
def load_and_process_documents(url):
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    return text_splitter.split_documents(documents)

def load_and_process_local_documents(filepath):
    if filepath.lower().endswith('.pdf'):
        text = load_pdf_documents(filepath)
    elif filepath.lower().endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        raise ValueError("Unsupported file format. Only PDF and TXT files are supported.")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    return text_splitter.create_documents([text])

# Load PDF content
def load_pdf_documents(filepath):
    with fitz.open(filepath) as doc:
        texts = [page.get_text() for page in doc]
    return "\n".join(texts)

def save_embeddings(vector_store, file_path):
    """
    Save embeddings and metadata from FAISS vector store to a JSON file.
    """
    data = {
        "embeddings": vector_store.serialize_index(),
        "documents": [doc.dict() for doc in vector_store.documents],
        "metadata": vector_store.metadata
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Embeddings saved to {file_path}")

def load_embeddings(file_path):
    """
    Load embeddings and metadata from a JSON file into a FAISS vector store.
    """
    global vector_store
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No embeddings file found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vector_store = FAISS.deserialize_index(data["embeddings"])
    vector_store.documents = [FAISS.Document(**doc) for doc in data["documents"]]
    vector_store.metadata = data["metadata"]
    print(f"Embeddings loaded from {file_path}")


def get_session_log_filename():
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    return f"log_incremental_iterator_{session_id}.txt"

session_log_file = get_session_log_filename()

def add_new_data_to_kb(new_data, chunk_size=700, chunk_overlap=50):
    """Add new data to the knowledge base."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = text_splitter.create_documents(new_data)
    vector_store.add_documents(documents)
    with open(session_log_file, "a", encoding="utf-8") as log_file:
        for doc in documents:
            log_file.write(doc.page_content + "\n")
            log_file.write("=" * 40 + "\n")  

def setup_retriever_and_qa(documents, save_path=None):
    """
    Configura el sistema de recuperación de información y el modelo de QA.
    """
    global vector_store
    embeddings = OpenAIEmbeddings()  

    if save_path and os.path.exists(f"{save_path}/index.faiss"):
        print("Loading embeddings from file...")
        vector_store = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Generating new embeddings...")
        vector_store = FAISS.from_documents(documents, embeddings)
        if save_path:
            vector_store.save_local(save_path)

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_template(RAG_prompts["context_query"])
    primary_qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    return retriever, prompt, primary_qa_llm

template = RAG_prompts["context_query"]
prompt = ChatPromptTemplate.from_template(template)
    
# Run RAG to get answer to a question
def get_rag_answer(question, retriever, primary_qa_llm):
    
    retrieval_augmented_qa_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": prompt | primary_qa_llm, "context": itemgetter("context")}
    )
    result = retrieval_augmented_qa_chain.invoke({"question": question})
    return result["response"].content

# def get_rag_answer(question):
#     time.sleep(10)
#     return question + " || content retrieved!"