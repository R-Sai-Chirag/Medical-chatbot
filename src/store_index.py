import os
from dotenv import load_dotenv
load_dotenv()
from src.helper import load_pdf_files,split_docs
from pinecone import Pinecone,ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

groq_api_key=os.getenv("GRQ_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY

extracted_data=load_pdf_files("C:/Users/saich/OneDrive/Desktop/chatbot/Medical-chatbot/data")
splits=split_docs(extracted_data)

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

pc=Pinecone(api_key=PINECONE_API_KEY)

index_name="nutri-gpt"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws",region="us-east-1")
    )

index=pc.Index(index_name)

doc_search=PineconeVectorStore.from_documents(
    documents=splits,
    embedding=embeddings,
    index_name=index_name
)
