from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
prompt1 = (
  " You are a professional AI prompt engineer specializing in nutrition. Your task is to take the user’s input prompt and enhance it to be clear, precise, and effective for a large language model, using only the information provided in the user’s prompt and any relevant context explicitly given. Follow these rules:"  
"1. **Use Only Provided Information:** Enhance the prompt strictly based on the user’s input and any provided context, without adding assumptions or external information. " 
"2. **Clarity & Precision:** Ensure the prompt is unambiguous, concise, and goal-oriented.  "
"3. **Stepwise Guidance:** If the task is complex, break it into clear steps or instructions. " 
"4. **Enhance Creativity:** Make the prompt expressive and insightful while staying strictly on-topic."  
"5. **Neutral & Safe:** Avoid biased, leading, or unsafe instructions.  "
"**Input:**  "
"User Prompt: {user_prompt}  "
"**Output:**  "
"Return only the enhanced, context-aware prompt ready to be used. Do not include explanations or extra text."
)



enhance_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt1),
    MessagesPlaceholder(variable_name="context"),
    ("human", "{user_prompt}")
])



groq_api_key=os.getenv("GRQ_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY



model1=ChatGroq(model="openai/gpt-oss-20b",groq_api_key=groq_api_key)



store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]



enhance_chain1 = RunnableWithMessageHistory(
    runnable=enhance_prompt|model1,
    get_session_history=get_session_history,
    input_messages_key="user_prompt",  
    history_messages_key="context"    
)


def enhance(query:str):
    enhanced_query=enhance_chain1.invoke({"user_prompt":query},
                                         config={"configurable":{"session_id":"default"}})
    return enhanced_query.content