from flask import Flask,render_template,jsonify,request
from src.helper import load_pdf_files,split_docs,get_session_history
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import HumanMessage, AIMessage
from src.prompt_enhancer import enhance
from dotenv import load_dotenv
from src.prompt import *
import os

app=Flask(__name__)


groq_api_key=os.getenv("GRQ_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")
os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

index_name="nutri-gpt"
doc_search=PineconeVectorStore.from_existing_index(index_name=index_name,
                                                   embedding=embeddings)

retriever=doc_search.as_retriever(search_type="similarity",search_kwargs={"k":3})

model=ChatGroq(model="openai/gpt-oss-20b",groq_api_key=groq_api_key)

context_prompt=ChatPromptTemplate.from_messages([
    ("system",context_system_prompt),
    MessagesPlaceholder("history"),
    ("human","{input}")
])

history_retriever=create_history_aware_retriever(model,retriever,context_prompt)

prompt=ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    MessagesPlaceholder("history"),
    ("human","{input}")]
)

chain=create_stuff_documents_chain(prompt=prompt,llm=model)

rag_chain=create_retrieval_chain(history_retriever,chain)



rag_chain=RunnableWithMessageHistory(rag_chain,get_session_history,
                                     input_messages_key="input",
                                     history_messages_key="history",
                                     output_messages_key="answer",
)



@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get",methods=["GET","POST"])
def chat():
    msg=request.form["msg"]
    input=msg
    print(input)
    response=rag_chain.invoke({"input":msg},
                              {"configurable":{"session_id":"default"}})
    print("Response : ",response)
    return response["answer"]

@app.route("/enhance",methods=["POST"])
def enhance_message():
    user_msg=request.form.get("msg")
    enhanced=enhance(user_msg)
    return enhanced

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
