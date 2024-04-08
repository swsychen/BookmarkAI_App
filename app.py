# 
# Copyright (c) 2024 swsychen.
# All rights reserved. Licensed under the MIT license.
# See LICENSE file in the project root for details.
#
import os

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_community import vectorstores
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA,RetrievalQAWithSourcesChain

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "OPENAI_API_KEY"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or "PINECONE_API_KEY"
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") or "PINECONE_ENVIRONMENT"

model_name = "text-embedding-ada-002"
text_field = "flow_document"  # default value for estuary flow 
index_name = "YOUR_INDEX_NAME"  # Replace with your index name
namespace = ""  # Replace with your namespace name, empty for free tier


def configure_retriever(model_name,openai_api_key,pinecone_api_key,namespace,index_name,text_field,stream_handler):
    
    embed = OpenAIEmbeddings(model=model_name, openai_api_key=openai_api_key)
    vectorstore= PineconeVectorStore(
            pinecone_api_key=pinecone_api_key,namespace=namespace,index_name=index_name,embedding=embed,text_key=text_field
        )
    llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
    
    retriever = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever(search_kwargs={'k': 10}))

    return retriever


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key=OPENAI_API_KEY

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        
        qa=configure_retriever(model_name,openai_api_key,PINECONE_API_KEY,namespace,index_name,text_field,stream_handler)
        response = qa.invoke(prompt)
        # print(response)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response['result']))