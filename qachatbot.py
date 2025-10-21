import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate
import os


## Page config
st.set_page_config("simple langchain chatbot with groq",page_icon="rocket")

# title
st.title("Groq simple langchain chat with groq")
st.markdown("Learn Langchain basics with Groq's ultra-fast inference!")

with st.sidebar:
    st.header("Settings")

    ##Api key
    api_key=st.text_input("GROQ_API_KEY",type="password",help="GET free API key at console.groq.com")


    ###
    model_name=st.selectbox(
        "model",
        ["llama-8b-8192","llama-3.1-8b-instant"],
        index=1
    )

    if st.button("clear chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages=[]

##Initialize llm
@st.cache_resource
def get_chain(api_key,model_name):
    if not api_key:
        return None
    
    ##Initialize the GROQ Model
    llm = ChatGroq(api_key=api_key,model_name=model_name,temperature=0.7,streaming=True)

    #Template for story analysis
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","you are an helpful assistant powered by groq. answer questions clearly and consisely"),
            ("user", "{question}")
        ]
    ) 

    ##create chain
    chain = prompt | llm | StrOutputParser

    return chain

chain = get_chain(api_key,model_name)

if not chain:
    st.warning("please enter correct groq api key")
    st.markdown("get your api key from here")

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    ## chat input
    if question:= st.chat_input("ask me anything"):

        st.session_state.message.append({"role":"user","content":question})
        with st.chat_message("user"):
            st.write(question)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:

            for chunk in chain.stream({"question":question}):
                full_response += chunk
                message_placeholder.markdown(full_response + "|")

            message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role":"assistant","content": full_response})

        except Exception as e:
            st.error(f"Error: {str(e)}")



