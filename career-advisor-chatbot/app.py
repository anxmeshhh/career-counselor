from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.utilities import SerpAPIWrapper

import streamlit as st
from dotenv import load_dotenv
import emoji

import os
from itertools import zip_longest


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


st.title(f"Career Advisor Chatbot {emoji.emojize(':robot:')}")

global vectors
# Define your directory containing PDF files here
pdf_dir = 'pdf'

if "pdf_texts" not in st.session_state:
    temp_pdf_texts = []
    with st.spinner("Creating a Database..."):
        for file in os.listdir(pdf_dir):
            if file.endswith('.pdf'):
                loader = PyPDFLoader(os.path.join(pdf_dir, file))
                documents = loader.load()
                text = " ".join([doc.page_content for doc in documents])
                temp_pdf_texts.append(text)
        st.session_state["pdf_texts"] = temp_pdf_texts
        pdf_list = list(st.session_state["pdf_texts"])
        pdfDatabase = " ".join(pdf_list)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(pdfDatabase)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        google_api_key=os.getenv("GOOGLE_API_KEY")

        if "vectors" not in st.session_state: 
            vectors = FAISS.from_texts(chunks, embeddings)
            st.session_state["vectors"] = vectors
    st.success("Database creation completed!")

def get_response(history,user_message,temperature=0):

    DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an Career Advisor. The Advisor guides the user regaring jobs,interests and other domain selection decsions.
    It follows the previous conversation to do so

    Relevant pieces of previous conversation:
    {context},

    Useful information from career guidance books:
    {text}, 

    Useful information about career guidance from Web:
    {web_knowledge},

    Current conversation:
    Human: {input}
    Career Expert:"""

    PROMPT = PromptTemplate(
        input_variables=['context','input','text','web_knowledge'], template=DEFAULT_TEMPLATE
    )
    docs = st.session_state["vectors"].similarity_search(user_message)


    params = {
    "engine": "google",
    "gl": "us",
    "hl": "en",
    }

    search = SerpAPIWrapper(params=params)

    web_knowledge=search.run(user_message)


    gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)

    conversation_with_summary = LLMChain(
        llm=gemini_model,
        prompt=PROMPT,
        verbose=False
    )
    response = conversation_with_summary.predict(context=history,input=user_message,web_knowledge=web_knowledge,text = docs)
    return response

# Function to get conversation history
def get_history(history_list):
    history = ''
    for message in history_list:
        if message['role']=='user':
            history = history+'input '+message['content']+'\n'
        elif message['role']=='assistant':
            history = history+'output '+message['content']+'\n'
    
    return history


# Streamlit UI
def get_text():
    input_text = st.sidebar.text_input("You: ", "Hello, how are you?", key="input")
    if st.sidebar.button('Send'):
        return input_text
    return None

if "past" not in st.session_state:
    st.session_state["past"] = []
if "generated" not in st.session_state:
    st.session_state["generated"] = []

user_input = get_text()

if user_input:
    user_history = list(st.session_state["past"])
    bot_history = list(st.session_state["generated"])

    combined_history = []
    for user_msg, bot_msg in zip_longest(user_history, bot_history):
        if user_msg is not None:
            combined_history.append({'role': 'user', 'content': user_msg})
        if bot_msg is not None:
            combined_history.append({'role': 'assistant', 'content': bot_msg})

    formatted_history = get_history(combined_history)

    output = get_response(formatted_history,user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

with st.expander("Chat History", expanded=True):
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            st.markdown(emoji.emojize(f":speech_balloon: **User {str(i)}**: {st.session_state['past'][i]}"))
            st.markdown(emoji.emojize(f":robot: **Assistant {str(i)}**: {st.session_state['generated'][i]}"))


# what factors should I keep in mind before deciding a career?

# What are the growing sectors of global economy ?

# If I decide to be a software engineer what would My salary be ?


