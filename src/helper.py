from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()

def load_pdf_files(data):
    loader=DirectoryLoader(data,loader_cls=PyPDFLoader,glob="*.pdf")
    docs=loader.load()
    return docs

def split_docs(docs:list[Document]):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
    splits=splitter.split_documents(docs)
    return splits

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

store={}
def get_session_history(session_id:str):
            if session_id not in store:
                store[session_id]=ChatMessageHistory()
            return store[session_id]