import streamlit as st 
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

##LangSmith Tracking
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")  ###Used for LangSmith tracking
os.environ['LANGCHAIN_TRACING_V2'] ="true"
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")

##Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistnat, Please respons to user questions"),
    ("user","Question:{question}")
])

def generate_response(question,llm,temparature,max_tokens):
    llm = ChatOpenAI(model=llm,temparature=temparature,max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer

#Title of the app
st.title("Enhanced Q&A chatbot with OpenAI")

st.sidebar.title("Settings")

llm = st.sidebar.selectbox("Select Open AI Models",["gpt-4o","gpt-4-turbo","gpt-4"])
temparature = st.sidebar.slider("Temparature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)



##Main interface for user inputs
st.write("Go ahead and ask any questions")
user_input = st.text_input("You:")
if user_input:
    response = generate_response(user_input,llm,temparature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")