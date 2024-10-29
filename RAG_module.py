import os
import json
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
from RAG_prompts import en_prompts, es_prompts

# Load OpenAI API key
def setup_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        auth_path = os.path.expanduser("~/.openai/auth.json")
        if os.path.exists(auth_path):
            with open(auth_path, 'r') as file:
                data = json.load(file)
                api_key = data.get('api_key')
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key

# Load and split documents from a URL
def load_and_process_documents(url):
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    return text_splitter.split_documents(documents)

# Load and split local PDF documents
def load_and_process_local_documents(filepath):
    text = load_pdf_documents(filepath)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
    return text_splitter.create_documents([text])

# Load PDF content
def load_pdf_documents(filepath):
    with fitz.open(filepath) as doc:
        texts = [page.get_text() for page in doc]
    return "\n".join(texts)

# Setup retriever and QA components
def setup_retriever_and_qa(documents, language="es"):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector_store = FAISS.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever()
    
    prompt_template = en_prompts["context_query"] if language == "en" else es_prompts["context_query"]
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    primary_qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    return retriever, prompt, primary_qa_llm

# Run RAG to get answer to a question
def get_rag_answer(question, retriever, prompt, primary_qa_llm):
    retrieval_augmented_qa_chain = (
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(context=itemgetter("context"))
        | {"response": prompt | primary_qa_llm, "context": itemgetter("context")}
    )
    result = retrieval_augmented_qa_chain.invoke({"question": question})
    return result["response"].content
    return "content retreived!"

def get_rag_answer(question):
    time.sleep(10)
    return question + " || content retrieved!"