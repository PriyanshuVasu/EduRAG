import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage

from database import get_user_history # Changed from get_session_history

load_dotenv()

DB_PATH = "./chroma_db"
MODEL_NAME = "gemini-2.5-flash-lite"

llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", transport="rest")
vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

condense_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given the conversation, rephrase the follow-up question to be a standalone question."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert educational tutor. Answer the user's question based on the context provided. Be concise and clear.\n\nContext:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

def format_chat_history(chat_history):
    return [
        HumanMessage(content=msg["content"]) if msg["role"] == "user"
        else AIMessage(content=msg["content"])
        for msg in chat_history
    ]

def get_conversational_rag_chain():
    _standalone_question = RunnablePassthrough.assign(
        chat_history=lambda x: format_chat_history(get_user_history(x["user_id"]))
    ) | condense_prompt | llm

    conversational_rag_chain = (
        RunnablePassthrough.assign(standalone_question=_standalone_question)
        | RunnablePassthrough.assign(
            context=lambda x: retriever.invoke(x["standalone_question"].content)
        )
        | RunnablePassthrough.assign(
            chat_history=lambda x: format_chat_history(get_user_history(x["user_id"]))
        )
        | {
            "context": lambda x: x["context"],
            "question": lambda x: x["standalone_question"].content,
            "chat_history": lambda x: x["chat_history"],
        }
        | answer_prompt
        | llm
    )
    
    return conversational_rag_chain

rag_chain = get_conversational_rag_chain()